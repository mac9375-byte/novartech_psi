"""BOM 업무 규칙 (Ⅵ-3)."""
from collections import defaultdict

from core import lookup
from core.excel import ERROR, INFO, WARNING, issue, read_sheet, to_code, to_fraction, to_text

from .models import BomLine, BomVersion

MODULE, SHEET = "M3", "BOM"
H_CUST, H_MAT, H_UNIT, H_QTY = "Customer Code", "Material Code", "Unit", "Q'ty"
ASSY = "ASSY"
UPLOAD_TYPES = {"ADD": "Add (등록): add new Assy BOMs only", "CHANGE": "Change (변경): replace BOM of Assy in file"}
COUNT_LABELS = [("new", "New BOM (신규)"), ("changed", "Replaced (교체)"), ("skipped", "Skipped (무시)"),
                ("unchanged", "No change (변경 없음)"), ("ignored", "Ignored Assy (자재 열 없음)")]


def current_versions(codes=None):
    qs = BomVersion.objects.filter(is_current=True)
    if codes is not None:
        qs = qs.filter(customer_code__in=list(codes))
    return {v.customer_code: v for v in qs.prefetch_related("lines")}


def registered(codes=None):
    """BOM 등록 Assy: Assy 열 1개 + 자재 열 1개 이상 (Ⅵ-6-5). 현재 BOM은 항상 자재 행이 있다."""
    return set(current_versions(codes))


def bom_map():
    """계산용: {Customer Code: {Material Code: 소요원수 합계(Fraction)}} (같은 자재 여러 행 합산, M-1)."""
    out = defaultdict(lambda: defaultdict(int))
    for line in BomLine.objects.filter(version__is_current=True).select_related("version"):
        out[line.version.customer_code][line.material_code] += line.qty
    return {k: dict(v) for k, v in out.items()}


def _line_key(lines):
    return [(l["mat"], l["unit"], l["num"], l["den"]) for l in lines]


def validate(fileobj, upload_type, week):
    raw_rows, issues = read_sheet(fileobj, SHEET, [H_CUST, H_MAT, H_UNIT, H_QTY])
    mats = lookup.materials()
    from materials.models import UnitCode
    units = set(UnitCode.objects.values_list("code", flat=True))
    blocks, order, done = {}, [], set()
    cur = None
    for raw in raw_rows:
        n = raw["_row"]
        try:
            cust, mat = to_code(raw.get(H_CUST)), to_code(raw.get(H_MAT))
        except ValueError as e:
            issues.append(issue(ERROR, SHEET, n, H_CUST + "/" + H_MAT, str(e)))
            continue
        if not cust or not mat:
            issues.append(issue(ERROR, SHEET, n, H_CUST if not cust else H_MAT, "Value is required.", cust or ""))
            continue
        if cust != cur:
            if cust in done or cust in blocks:
                issues.append(issue(ERROR, SHEET, n, H_CUST, "Rows of the same Customer Code must be "
                                    "continuous. (같은 Customer Code 행은 연속되어야 합니다.)", cust))
                cur = None
                continue
            if cur:
                done.add(cur)
            cur = cust
            if mat != ASSY:
                issues.append(issue(ERROR, SHEET, n, H_MAT, "A BOM must start with an Assy row "
                                    "(Material Code = 'Assy'). (Assy 열 없이 자재 열이 나왔습니다.)", cust))
                cur = None
                continue
            blocks[cust] = {"code": cust, "row": n, "lines": []}
            order.append(cust)
            continue
        if mat == ASSY:
            issues.append(issue(ERROR, SHEET, n, H_MAT, "The Assy row appears twice for this Customer Code.", cust))
            continue
        unit = to_text(raw.get(H_UNIT))
        unit = unit.upper() if unit else None
        try:
            qty = to_fraction(raw.get(H_QTY))
        except ValueError as e:
            issues.append(issue(ERROR, SHEET, n, H_QTY, str(e), mat))
            continue
        if qty is None or qty <= 0:
            issues.append(issue(ERROR, SHEET, n, H_QTY, "Q'ty must be greater than 0.", mat))
            continue
        m = mats.get(mat)
        if not unit:
            issues.append(issue(ERROR, SHEET, n, H_UNIT, "Unit is required.", mat))
            continue
        if m and unit != m.unit_id:
            issues.append(issue(ERROR, SHEET, n, H_UNIT,
                                f"Unit '{unit}' differs from Material Master Unit '{m.unit_id}'.", mat))
            continue
        if not m:
            if unit not in units:
                issues.append(issue(ERROR, SHEET, n, H_UNIT, f"'{unit}' is not an allowed Unit.", mat))
                continue
            issues.append(issue(WARNING, SHEET, n, H_MAT, "Not in Material Master (No DB). Unit not compared.", mat))
        blocks[cust]["lines"].append({"row": n, "mat": mat, "unit": unit,
                                      "num": qty.numerator, "den": qty.denominator})

    assies = lookup.assies(order)
    existing = current_versions(order)
    counts = {"new": 0, "changed": 0, "skipped": 0, "unchanged": 0, "ignored": 0}
    rows, details = [], []
    for code in order:
        b = blocks[code]
        if not b["lines"]:
            counts["ignored"] += 1
            issues.append(issue(INFO, SHEET, b["row"], H_MAT, "No material rows; ignored, existing BOM kept.", code))
            continue
        if code not in assies:
            issues.append(issue(WARNING, SHEET, b["row"], H_CUST, "Not in Assy Master (No DB).", code))
        old = existing.get(code)
        if not old:
            kind = "new"
        elif upload_type == "ADD":
            kind = "skipped"
        else:
            old_key = [(l.material_code, l.unit, l.qty_num, l.qty_den) for l in old.lines.all()]
            kind = "unchanged" if old_key == _line_key(b["lines"]) else "changed"
        counts[kind] += 1
        if kind in ("new", "changed"):
            rows.append(b)
            details.append({"kind": kind, "code": code, "row": b["row"],
                            "changes": [f"{len(b['lines'])} material row(s)"]})
    return rows, len(raw_rows), issues, counts, details


def apply(batch, user):
    """Change는 파일의 Assy만 교체(기존 BOM은 History), 파일에 없는 Assy는 유지 (Ⅵ-3-8)."""
    codes = [b["code"] for b in batch.preview_rows]
    assies, mats = lookup.assies(codes), lookup.materials()
    existing = current_versions(codes)
    for b in batch.preview_rows:
        old = existing.get(b["code"])
        if old:
            if batch.upload_type == "ADD":
                continue
            old.is_current = False
            old.save(update_fields=["is_current"])
        a = assies.get(b["code"])
        v = BomVersion.objects.create(customer_code=b["code"], updated_by=user, upload_batch=batch,
                                      assy_type=a.assy_type if a else None, model_name=a.model_name if a else None,
                                      item=a.item if a else None)
        BomLine.objects.bulk_create([
            BomLine(version=v, seq=i, material_code=l["mat"], unit=l["unit"], qty_num=l["num"], qty_den=l["den"],
                    desc_snap=getattr(mats.get(l["mat"]), "description", None),
                    spec_snap=getattr(mats.get(l["mat"]), "spec", None))
            for i, l in enumerate(b["lines"], start=1)])
