"""Safety Stock 업무 규칙 (Ⅵ-4): 파일로 전체교체, 변경분만 History."""
from django.utils import timezone

from core import lookup
from core.excel import ERROR, WARNING, issue, read_sheet, to_code, to_int

from .models import SafetyHistory, SafetyStock

MODULE, SHEET = "M4", "SAFETY"
H_CUST, H_QTY = "Customer Code", "Safety Q'ty"
COUNT_LABELS = [("new", "Added (추가)"), ("changed", "Changed (변경)"), ("deleted", "Deleted (삭제)"),
                ("unchanged", "No change (변경 없음)")]


def safety_map():
    return dict(SafetyStock.objects.values_list("customer_code", "qty"))


def validate(fileobj, upload_type, week):
    from bom.services import registered
    raw_rows, issues = read_sheet(fileobj, SHEET, [H_CUST, H_QTY])
    seen, rows = {}, []
    for raw in raw_rows:
        n = raw["_row"]
        try:
            code = to_code(raw.get(H_CUST))
        except ValueError as e:
            issues.append(issue(ERROR, SHEET, n, H_CUST, str(e)))
            continue
        if not code:
            issues.append(issue(ERROR, SHEET, n, H_CUST, "Customer Code is required."))
            continue
        if code in seen:
            issues.append(issue(ERROR, SHEET, n, H_CUST, f"Duplicate Customer Code (also in row {seen[code]}). "
                                "Not summed.", code))
            continue
        seen[code] = n
        try:
            qty = to_int(raw.get(H_QTY))
            qty = 0 if qty is None else qty                      # 빈 Cell = 0
            if qty < 0:
                raise ValueError("Must be a whole number.")
        except ValueError as e:
            issues.append(issue(ERROR, SHEET, n, H_QTY, f"Safety Q'ty must be a whole number of 0 or more. ({e})", code))
            continue
        rows.append({"row": n, "code": code, "qty": qty})

    codes = [r["code"] for r in rows]
    assies, boms = lookup.assies(codes), registered(codes)
    for r in rows:
        a = assies.get(r["code"])
        if not a:
            issues.append(issue(WARNING, SHEET, r["row"], H_CUST, "Not in Assy Master (No DB); included in calculation.", r["code"]))
        elif a.status == "INACTIVE":
            issues.append(issue(WARNING, SHEET, r["row"], H_CUST, "Inactive Assy; included in calculation.", r["code"]))
        if r["code"] not in boms:
            issues.append(issue(WARNING, SHEET, r["row"], H_CUST, "No BOM; requirement is counted as 0.", r["code"]))

    old = safety_map()
    new = {r["code"]: r["qty"] for r in rows}
    counts = {"new": sum(c not in old for c in new), "changed": sum(c in old and old[c] != q for c, q in new.items()),
              "deleted": sum(c not in new for c in old), "unchanged": sum(old.get(c) == q for c, q in new.items())}
    details = ([{"kind": "new", "code": c, "row": "", "changes": [f"{q}"]} for c, q in new.items() if c not in old]
               + [{"kind": "changed", "code": c, "row": "", "changes": [f"{old[c]} → {q}"]}
                  for c, q in new.items() if c in old and old[c] != q]
               + [{"kind": "deleted", "code": c, "row": "", "changes": [f"{q} → (deleted)"]}
                  for c, q in old.items() if c not in new])
    return rows, len(raw_rows), issues, counts, details


def apply(batch, user):
    """전체교체. 실제로 바뀐 행만 Update 갱신·History 기록 (같은 내용 재Upload는 이력 없음)."""
    now = timezone.now()
    new = {r["code"]: r["qty"] for r in batch.preview_rows}
    current = {s.customer_code: s for s in SafetyStock.objects.all()}
    hist = []
    for code, s in current.items():
        if code not in new:
            hist.append(SafetyHistory(customer_code=code, qty=s.qty, change_type="Delete"))
            s.delete()
        elif s.qty != new[code]:
            s.qty, s.updated_at, s.updated_by = new[code], now, user
            s.save()
            hist.append(SafetyHistory(customer_code=code, qty=s.qty, change_type="Change"))
    for code, qty in new.items():
        if code not in current:
            SafetyStock.objects.create(customer_code=code, qty=qty, updated_at=now, updated_by=user)
            hist.append(SafetyHistory(customer_code=code, qty=qty, change_type="Add"))
    for h in hist:
        h.changed_at, h.changed_by, h.upload_batch = now, user, batch
    SafetyHistory.objects.bulk_create(hist)
