"""Weekly Data 업무 규칙 (Ⅵ-5 Inventory, Ⅵ-6 RTF/Prod., Ⅵ-7 Open PO, Ⅵ-8 Scheduled Receipt).

Upload는 항상 Current Week(작업 주차 W0) 데이터만 전체교체하고, 과거 주차는 건드리지 않는다.
"""
from collections import defaultdict
from datetime import date, datetime
from decimal import Decimal

from core import lookup, weeks
from core.excel import ERROR, WARNING, issue, read_sheet, to_code, to_decimal, to_int, to_text

from .models import InventoryRow, OpenPoRow, PlanRow, SchedRow

ZERO = Decimal(0)
CURRENCIES = ("USD", "KRW", "VND", "CNY", "JPY")
REPLACE_LABELS = [("rows", "Rows to save (저장 행)"), ("replaced", "Existing rows replaced (기존 행 교체)")]


def vkey(vendor):
    return (vendor or "").strip().upper()


def _units():
    from materials.models import UnitCode
    return set(UnitCode.objects.values_list("code", flat=True))


def _material_unit_issue(sheet, n, code, unit, mats, units, field="Unit"):
    """Material 행 Unit 검사: Master에 있으면 같아야 함(Error), 없으면 'No DB' Warning (Ⅳ-7-10)."""
    if not unit:
        return issue(ERROR, sheet, n, field, "Unit is required.", code), None
    m = mats.get(code)
    if m and unit != m.unit_id:
        return issue(ERROR, sheet, n, field, f"Unit '{unit}' differs from Material Master Unit '{m.unit_id}'.", code), None
    if not m:
        if unit not in units:
            return issue(ERROR, sheet, n, field, f"'{unit}' is not an allowed Unit.", code), None
        return None, issue(WARNING, sheet, n, "Material Code", "Not in Material Master (No DB).", code)
    if m.status == "INACTIVE":
        return None, issue(WARNING, sheet, n, "Material Code", "Inactive Material; included in calculation.", code)
    return None, None


def _assy_warning(sheet, n, code, assies):
    a = assies.get(code)
    if not a:
        return issue(WARNING, sheet, n, "Customer Code", "Not in Assy Master (No DB); included in calculation.", code)
    if a.status == "INACTIVE":
        return issue(WARNING, sheet, n, "Customer Code", "Inactive Assy; included in calculation.", code)
    return None


def _qty(raw, places=6, integer=False):
    """수량: 빈칸 = 0, 음수 불가."""
    v = to_int(raw) if integer else to_decimal(raw, places)
    v = 0 if v is None else v
    if v < 0:
        raise ValueError("Negative values are not allowed.")
    return v


def _week_headers_issue(sheet, issues, week):
    hz = weeks.horizon(week)
    if any(i["level"] == ERROR and i["field"] in hz for i in issues):
        issues.append(issue(ERROR, sheet, 1, "Week columns",
                            f"Week headers must be 14 consecutive weeks from the working week: {hz[0]} ~ {hz[-1]} "
                            "(YYYY-Www)."))


# ---------------- Module 5 Inventory ----------------
INV_SHEET = "INVENTORY"
INV_H = ["Category", "Code", "Unit", "Stock Q'ty"]


def inventory_validate(fileobj, upload_type, week):
    raw_rows, issues = read_sheet(fileobj, INV_SHEET, INV_H)
    mats, assies, units = lookup.materials(), lookup.assies(), _units()
    seen, rows = {}, []
    for raw in raw_rows:
        n = raw["_row"]
        cat = (to_text(raw.get("Category")) or "").upper()
        if cat not in ("ASSY", "MATERIAL"):
            issues.append(issue(ERROR, INV_SHEET, n, "Category", "Category must be 'Assy' or 'Material'."))
            continue
        try:
            code = to_code(raw.get("Code"))
        except ValueError as e:
            issues.append(issue(ERROR, INV_SHEET, n, "Code", str(e)))
            continue
        if not code:
            issues.append(issue(ERROR, INV_SHEET, n, "Code", "Code is required."))
            continue
        if (cat, code) in seen:
            issues.append(issue(ERROR, INV_SHEET, n, "Code", f"Duplicate Category + Code (also in row {seen[cat, code]}). "
                                "Not summed.", code))
            continue
        seen[cat, code] = n
        try:
            qty = _qty(raw.get("Stock Q'ty"))
        except ValueError as e:
            issues.append(issue(ERROR, INV_SHEET, n, "Stock Q'ty", f"Stock Q'ty must be 0 or more. ({e})", code))
            continue
        unit = (to_text(raw.get("Unit")) or "").upper()
        if cat == "ASSY":
            if unit not in ("", "EA"):
                issues.append(issue(ERROR, INV_SHEET, n, "Unit", "Assy Unit must be blank or 'EA'.", code))
                continue
            unit, warn = "EA", _assy_warning(INV_SHEET, n, code, assies)
        else:
            err, warn = _material_unit_issue(INV_SHEET, n, code, unit, mats, units)
            if err:
                issues.append(err)
                continue
        if warn:
            issues.append(warn)
        rows.append({"cat": cat, "code": code, "unit": unit, "qty": str(qty)})
    old = InventoryRow.objects.filter(week=week).count()
    return rows, len(raw_rows), issues, {"rows": len(rows), "replaced": old}, []


def inventory_apply(batch, user):
    InventoryRow.objects.filter(week=batch.week).delete()
    InventoryRow.objects.bulk_create([InventoryRow(week=batch.week, category=r["cat"], code=r["code"], unit=r["unit"],
                                                   qty=Decimal(r["qty"])) for r in batch.preview_rows])


# ---------------- Module 6 RTF / Production Plan ----------------
PLAN_SHEETS = {"RTF": "RTF", "PROD": "PROD_PLAN"}
PLAN_VALUES = {"RTF": ("RTF",), "PROD": ("PROD.", "PRODUCTION")}
PLAN_LABELS = [("rtf", "RTF rows"), ("prod", "Prod. rows"), ("replaced", "Existing rows replaced (기존 행 교체)")]


def plan_validate(fileobj, upload_type, week):
    """RTF와 PROD_PLAN 시트 중 있는 시트만 그 Plan을 교체한다 (Ⅵ-6-7)."""
    from bom.services import registered
    hz = weeks.horizon(week)
    issues, rows, sheets, total = [], [], [], 0
    for plan, sheet in PLAN_SHEETS.items():
        fileobj.seek(0)
        raw_rows, sheet_issues = read_sheet(fileobj, sheet, ["Customer Code", "Plan", *hz])
        if sheet_issues and sheet_issues[0]["field"] == "Sheet":
            continue                                   # 이 시트는 파일에 없음
        sheets.append(plan)
        _week_headers_issue(sheet, sheet_issues, week)
        issues.extend(sheet_issues)
        total += len(raw_rows)
        seen = {}
        for raw in raw_rows:
            n = raw["_row"]
            try:
                code = to_code(raw.get("Customer Code"))
            except ValueError as e:
                issues.append(issue(ERROR, sheet, n, "Customer Code", str(e)))
                continue
            if not code:
                issues.append(issue(ERROR, sheet, n, "Customer Code", "Customer Code is required."))
                continue
            if code in seen:
                issues.append(issue(ERROR, sheet, n, "Customer Code", f"Duplicate Customer Code (also in row {seen[code]}). "
                                    "Not summed.", code))
                continue
            seen[code] = n
            pv = (to_text(raw.get("Plan")) or "").upper()
            if pv not in PLAN_VALUES[plan]:
                allowed = "'RTF'" if plan == "RTF" else "'Prod.' or 'Production'"
                issues.append(issue(ERROR, sheet, n, "Plan", f"Plan must be {allowed} in sheet {sheet}.", code))
                continue
            qty, bad = [], False
            for w in hz:
                try:
                    qty.append(_qty(raw.get(w), integer=True))
                except ValueError as e:
                    issues.append(issue(ERROR, sheet, n, w, f"Must be a whole number of 0 or more. ({e})", code))
                    bad = True
            if not bad:
                rows.append({"plan": plan, "code": code, "qty": qty, "row": n, "sheet": sheet})
    if not sheets:
        issues.append(issue(ERROR, "RTF / PROD_PLAN", "", "Sheet", "Sheet 'RTF' or 'PROD_PLAN' not found."))
    assies, boms = lookup.assies({r["code"] for r in rows}), registered({r["code"] for r in rows})
    for r in rows:
        w = _assy_warning(r["sheet"], r["row"], r["code"], assies)
        if w:
            issues.append(w)
        if sum(r["qty"]) > 0 and r["code"] not in boms:
            issues.append(issue(WARNING, r["sheet"], r["row"], "Customer Code",
                                "No BOM: requirement counted as 0 (BOM 미등록).", r["code"]))
    old = PlanRow.objects.filter(week=week, plan__in=sheets).count()
    counts = {"rtf": sum(r["plan"] == "RTF" for r in rows), "prod": sum(r["plan"] == "PROD" for r in rows),
              "replaced": old, "sheets": sheets}
    return rows, total, issues, counts, []


def regenerate_auto_plans(week, safety_codes=()):
    """자동 생성 규칙 (M6-1): A) 한쪽 Plan만 있으면 다른 쪽을 0으로 생성. B) Safety Stock에만 있는 Code는
    RTF·Prod. 모두 0으로 생성 (Recalculate 시, safety_codes 전달). 생성 건수를 돌려준다."""
    PlanRow.objects.filter(week=week, auto=True).delete()
    manual = defaultdict(set)
    for plan, code in PlanRow.objects.filter(week=week).values_list("plan", "customer_code"):
        manual[plan].add(code)
    zeros = [0] * weeks.HORIZON
    new = [PlanRow(week=week, plan=other, customer_code=code, qty=zeros, auto=True)
           for plan, other in (("RTF", "PROD"), ("PROD", "RTF"))
           for code in manual[plan] - manual[other]]
    both = manual["RTF"] | manual["PROD"]
    new += [PlanRow(week=week, plan=p, customer_code=code, qty=zeros, auto=True)
            for code in set(safety_codes) - both for p in ("RTF", "PROD")]
    PlanRow.objects.bulk_create(new)
    return len(new)


def plan_apply(batch, user):
    PlanRow.objects.filter(week=batch.week, plan__in=batch.summary["sheets"]).delete()
    PlanRow.objects.bulk_create([PlanRow(week=batch.week, plan=r["plan"], customer_code=r["code"], qty=r["qty"])
                                 for r in batch.preview_rows])
    regenerate_auto_plans(batch.week)   # 규칙 A: Upload 완료 시


# ---------------- Module 7 Open PO ----------------
PO_SHEET = "OPEN_PO"
PO_REQ = ["PO Date", "PO No", "Material Code", "Unit", "PO Q'ty", "Vendor"]
PO_OPT = ["Currency", "Unit Price", "Cancel", "G/R", "In Transit"]


def _po_date(v):
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    s = to_text(v)
    try:
        return datetime.strptime(s or "", "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("PO Date must be a date (yyyy-mm-dd).")


def open_po_by_key(rows):
    """Material + Vendor별 Open PO 합계 = Σ(In Transit + Remain Q'ty), 합이 0보다 큰 행만 (H-3)."""
    out = defaultdict(lambda: ZERO)
    for r in rows:
        if r.open_qty > 0:
            out[r.material_code, vkey(r.vendor)] += r.open_qty
    return out


def _sched_over_po_issues(sched_sum, po_sum, sheet):
    """입고예정 14주 합계 > Open PO 이면 Error (Ⅶ-10, SR-2)."""
    return [issue(ERROR, sheet, "", "Material + Vendor",
                  f"Scheduled Receipt 14-week total {s:,} is greater than Open PO {po_sum.get(k, ZERO):,} "
                  "(In Transit + Remain). Fix Open PO / Scheduled Receipt.", f"{k[0]} / {k[1]}")
            for k, s in sched_sum.items() if s > po_sum.get(k, ZERO)]


def openpo_validate(fileobj, upload_type, week):
    raw_rows, issues = read_sheet(fileobj, PO_SHEET, PO_REQ, PO_OPT)
    mats, units = lookup.materials(), _units()
    rows = []
    for raw in raw_rows:
        n, errs = raw["_row"], []
        try:
            mat = to_code(raw.get("Material Code"))
        except ValueError as e:
            issues.append(issue(ERROR, PO_SHEET, n, "Material Code", str(e)))
            continue
        if not mat:
            issues.append(issue(ERROR, PO_SHEET, n, "Material Code", "Material Code is required."))
            continue
        r = {"mat": mat, "po_no": to_text(raw.get("PO No")), "vendor": to_text(raw.get("Vendor")),
             "unit": (to_text(raw.get("Unit")) or "").upper()}
        try:
            r["po_date"] = _po_date(raw.get("PO Date")).isoformat()
        except ValueError as e:
            errs.append(("PO Date", str(e)))
        if not r["po_no"]:
            errs.append(("PO No", "PO No is required."))
        if not r["vendor"]:
            errs.append(("Vendor", "Vendor is required."))
        for h, key in (("PO Q'ty", "po_qty"), ("Unit Price", "unit_price"), ("Cancel", "cancel"), ("G/R", "gr"),
                       ("In Transit", "in_transit")):
            try:
                v = to_decimal(raw.get(h), 6)
                if v is not None and v < 0:
                    raise ValueError("Negative values are not allowed.")
                r[key] = None if v is None and key == "unit_price" else str(v if v is not None else ZERO)
            except ValueError as e:
                errs.append((h, str(e)))
        if "po_qty" in r and Decimal(r["po_qty"]) <= 0:
            errs.append(("PO Q'ty", "PO Q'ty must be greater than 0."))
        cur = (to_text(raw.get("Currency")) or "").upper() or None
        if cur and cur not in CURRENCIES:
            errs.append(("Currency", f"Currency must be one of {', '.join(CURRENCIES)}."))
        if r.get("unit_price") is not None and not cur:
            errs.append(("Currency", "Currency is required when Unit Price is entered."))
        r["currency"] = cur
        err, warn = _material_unit_issue(PO_SHEET, n, mat, r["unit"], mats, units)
        if err:
            issues.append(err)
        if not errs and all(k in r for k in ("po_qty", "cancel", "gr", "in_transit")):
            remain = Decimal(r["po_qty"]) - Decimal(r["cancel"]) - Decimal(r["gr"]) - Decimal(r["in_transit"])
            if remain < 0:
                errs.append(("Remain Q'ty", f"Remain Q'ty is negative ({remain:,}). Fix and upload again."))
        issues.extend(issue(ERROR, PO_SHEET, n, f, reason, mat) for f, reason in errs)
        if errs or err:
            continue
        if warn:
            issues.append(warn)
        rows.append(r)
    # Module 8과 함께 점검: 같은 주차 입고예정이 이 Open PO를 넘으면 Error
    po_sum = defaultdict(lambda: ZERO)
    for r in rows:
        po_sum[r["mat"], vkey(r["vendor"])] += Decimal(r["po_qty"]) - Decimal(r["cancel"]) - Decimal(r["gr"])
    sched_sum = {(s.material_code, s.vendor_key): sum(s.qty_dec) for s in SchedRow.objects.filter(week=week)}
    if not any(i["level"] == ERROR for i in issues):
        issues.extend(_sched_over_po_issues(sched_sum, po_sum, PO_SHEET + " ↔ SCHED_RECEIPT"))
    old = OpenPoRow.objects.filter(week=week).count()
    return rows, len(raw_rows), issues, {"rows": len(rows), "replaced": old}, []


def openpo_apply(batch, user):
    OpenPoRow.objects.filter(week=batch.week).delete()
    OpenPoRow.objects.bulk_create([OpenPoRow(
        week=batch.week, seq=i, po_date=r["po_date"], po_no=r["po_no"], material_code=r["mat"], unit=r["unit"],
        po_qty=Decimal(r["po_qty"]), currency=r["currency"],
        unit_price=None if r["unit_price"] is None else Decimal(r["unit_price"]),
        cancel=Decimal(r["cancel"]), gr=Decimal(r["gr"]), in_transit=Decimal(r["in_transit"]), vendor=r["vendor"],
    ) for i, r in enumerate(batch.preview_rows, start=1)])


# ---------------- Module 8 Scheduled Receipt ----------------
SR_SHEET = "SCHED_RECEIPT"


def sched_validate(fileobj, upload_type, week):
    hz = weeks.horizon(week)
    raw_rows, issues = read_sheet(fileobj, SR_SHEET, ["Material Code", "Vendor", "Unit", *hz])
    _week_headers_issue(SR_SHEET, issues, week)
    mats, units = lookup.materials(), _units()
    seen, rows = {}, []
    for raw in raw_rows:
        n = raw["_row"]
        try:
            mat = to_code(raw.get("Material Code"))
        except ValueError as e:
            issues.append(issue(ERROR, SR_SHEET, n, "Material Code", str(e)))
            continue
        vendor = to_text(raw.get("Vendor"))
        if not mat or not vendor:
            issues.append(issue(ERROR, SR_SHEET, n, "Material Code" if not mat else "Vendor", "Value is required.", mat or ""))
            continue
        key = (mat, vkey(vendor))
        if key in seen:
            issues.append(issue(ERROR, SR_SHEET, n, "Vendor", f"Duplicate Material + Vendor (also in row {seen[key]}). "
                                "Sum by week into one row.", mat))
            continue
        seen[key] = n
        qty, bad = [], False
        for w in hz:
            try:
                qty.append(_qty(raw.get(w)))
            except ValueError as e:
                issues.append(issue(ERROR, SR_SHEET, n, w, f"Must be 0 or more, up to 6 decimals. ({e})", mat))
                bad = True
        unit = (to_text(raw.get("Unit")) or "").upper()
        err, warn = _material_unit_issue(SR_SHEET, n, mat, unit, mats, units)
        if err:
            issues.append(err)
        if bad or err:
            continue
        if warn:
            if warn["reason"].startswith("Not in"):
                warn["reason"] += " Calculated Scheduled Receipt is skipped (no L/T)."
            issues.append(warn)
        rows.append({"mat": mat, "vendor": vendor, "unit": unit, "qty": [str(q) for q in qty]})
    if not any(i["level"] == ERROR for i in issues):
        po_sum = open_po_by_key(OpenPoRow.objects.filter(week=week))
        sched_sum = {(r["mat"], vkey(r["vendor"])): sum(Decimal(q) for q in r["qty"]) for r in rows}
        issues.extend(_sched_over_po_issues(sched_sum, po_sum, SR_SHEET))
    old = SchedRow.objects.filter(week=week).count()
    return rows, len(raw_rows), issues, {"rows": len(rows), "replaced": old}, []


def sched_apply(batch, user):
    SchedRow.objects.filter(week=batch.week).delete()
    SchedRow.objects.bulk_create([SchedRow(week=batch.week, material_code=r["mat"], vendor=r["vendor"],
                                           vendor_key=vkey(r["vendor"]), unit=r["unit"], qty=r["qty"])
                                  for r in batch.preview_rows])


def scheduled_receipts(week):
    """Material + Vendor별 입고예정: Manual(검정) + Calculated(파랑) (Ⅶ-11, 계층 2: 조회 시 실시간).

    차이분 = Open PO − Manual 14주 합계. > 0 이면 '작업 주차 + L/T' 주차(W+13 초과 시 W+13)에 합산.
    """
    po_rows = list(OpenPoRow.objects.filter(week=week))
    po = open_po_by_key(po_rows)
    it, rem = defaultdict(lambda: ZERO), defaultdict(lambda: ZERO)
    po_units, po_vendor = {}, {}
    for r in po_rows:
        if r.open_qty > 0:
            k = (r.material_code, vkey(r.vendor))
            it[k] += r.in_transit
            rem[k] += r.remain
            po_units.setdefault(k, r.unit)
            po_vendor.setdefault(k, r.vendor)
    manual = {(s.material_code, s.vendor_key): s for s in SchedRow.objects.filter(week=week)}
    mats = lookup.materials({k[0] for k in [*po, *manual]})
    out = {}
    for k in sorted(set(po) | set(manual)):
        s = manual.get(k)
        man = s.qty_dec if s else [ZERO] * weeks.HORIZON
        calc = [ZERO] * weeks.HORIZON
        diff = po.get(k, ZERO) - sum(man)
        m = mats.get(k[0])
        if diff > 0 and m:
            calc[min(m.lead_time_weeks, weeks.HORIZON - 1)] += diff
        out[k] = {"mat": k[0], "vendor": s.vendor if s else po_vendor[k], "unit": s.unit if s else po_units[k],
                  "manual": man, "calc": calc, "diff": diff, "in_transit": it.get(k, ZERO),
                  "remain": rem.get(k, ZERO), "material": m, "skipped": diff > 0 and not m}
    return out
