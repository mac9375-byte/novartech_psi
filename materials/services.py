"""Material Master 업무 규칙 (설계/01 B절, 설계/03).

Upload: validate() → plan() → (미리보기) → apply()
화면 수정: save_rows()
"""
from django.db import transaction
from django.utils import timezone

from accounts.models import User
from core.excel import ERROR, INFO, issue, read_sheet, to_code, to_int, to_text
from core.models import SystemStatus, UploadBatch

from .models import Material, MaterialHistory, Status, UnitCode

MODULE = "M1"
SHEET = "MD_Material"
ADD, CHANGE, INACTIVE = "ADD", "CHANGE", "INACTIVE"
UPLOAD_TYPES = {ADD: "Add", CHANGE: "Change", INACTIVE: "Inactive"}

H_CODE, H_DESC, H_SPEC, H_UNIT, H_PUR, H_VENDOR, H_COUNTRY, H_LT = (
    "Material Code", "Desc.", "Spec.", "Unit", "Purchaser ID", "Vendor", "Country", "L/T(Weeks)")
UPLOAD_HEADERS = [H_CODE, H_DESC, H_SPEC, H_UNIT, H_PUR, H_VENDOR, H_COUNTRY, H_LT]

# 비교·표시할 필드: (DB 필드, 화면/Excel 이름)
FIELDS = [("description", H_DESC), ("spec", H_SPEC), ("unit", H_UNIT), ("purchaser", "Purchaser"),
          ("vendor", H_VENDOR), ("country", H_COUNTRY), ("lead_time_weeks", H_LT)]


def current_values(m):
    return {"description": m.description, "spec": m.spec, "unit": m.unit_id,
            "purchaser": m.purchaser.username if m.purchaser else None,
            "vendor": m.vendor, "country": m.country, "lead_time_weeks": m.lead_time_weeks}


def diff(m, values):
    """바뀐 필드 목록 [(이름, 이전, 이후)]."""
    old = current_values(m)
    return [(label, old[f], values[f]) for f, label in FIELDS if old[f] != values[f]]


def _field_errors(values_in, units, usernames):
    """Add/Change 행의 필드 검증. (정규화된 값 dict, 오류 목록[(Column, 사유)])"""
    errors, v = [], {}
    unit = to_text(values_in.get(H_UNIT))
    unit = unit.upper() if unit else None
    if not unit:
        errors.append((H_UNIT, "Unit is required."))
    elif unit not in units:
        errors.append((H_UNIT, f"'{unit}' is not an allowed Unit ({', '.join(sorted(units))})."))
    purchaser = to_text(values_in.get(H_PUR))
    purchaser = purchaser.lower() if purchaser else None
    if purchaser and purchaser not in usernames:
        errors.append((H_PUR, f"'{purchaser}' is not a registered user ID."))
    try:
        lt = to_int(values_in.get(H_LT))
        if lt is None:
            errors.append((H_LT, "L/T(Weeks) is required."))
        elif lt < 1:
            errors.append((H_LT, "L/T(Weeks) must be 1 or more."))
    except ValueError as e:
        lt = None
        errors.append((H_LT, f"L/T(Weeks): {e}"))
    v.update(unit=unit, purchaser=purchaser, lead_time_weeks=lt,
             description=to_text(values_in.get(H_DESC)), spec=to_text(values_in.get(H_SPEC)),
             vendor=to_text(values_in.get(H_VENDOR)), country=to_text(values_in.get(H_COUNTRY)))
    return v, errors


def validate(fileobj, upload_type):
    """Excel을 읽고 검증한다. (통과 행 목록, 읽은 행 수, issues)"""
    required = [H_CODE] if upload_type == INACTIVE else [H_CODE, H_UNIT, H_LT]
    optional = [h for h in UPLOAD_HEADERS if h not in required]
    raw_rows, issues = read_sheet(fileobj, SHEET, required, optional)
    if upload_type == INACTIVE and raw_rows:
        issues.append(issue(INFO, SHEET, "", "", "Inactive upload: only 'Material Code' is used."))
    units = set(UnitCode.objects.values_list("code", flat=True))
    usernames = set(User.objects.values_list("username", flat=True))
    seen, rows = {}, []
    for raw in raw_rows:
        n = raw["_row"]
        try:
            code = to_code(raw.get(H_CODE))
        except ValueError as e:
            issues.append(issue(ERROR, SHEET, n, H_CODE, str(e), str(raw.get(H_CODE))))
            continue
        if not code:
            issues.append(issue(ERROR, SHEET, n, H_CODE, "Material Code is required."))
            continue
        if code == "ASSY":
            issues.append(issue(ERROR, SHEET, n, H_CODE, "'ASSY' cannot be used as a Material Code.", code))
            continue
        if code in seen:
            issues.append(issue(ERROR, SHEET, n, H_CODE,
                                f"Duplicate Material Code (also in row {seen[code]}). "
                                "Fix the Excel file and upload again.", code))
            continue
        seen[code] = n
        rec = {"row": n, "code": code}
        if upload_type != INACTIVE:
            values, errors = _field_errors(raw, units, usernames)
            if errors:
                issues.extend(issue(ERROR, SHEET, n, col, reason, code) for col, reason in errors)
                continue
            rec.update(values)
        rows.append(rec)
    return rows, len(raw_rows), issues


def plan(rows, upload_type):
    """DB 현재값과 비교해 각 행의 처리 방법을 정한다. (actions, counts)"""
    existing = {m.material_code: m for m in
                Material.objects.select_related("purchaser").filter(material_code__in=[r["code"] for r in rows])}
    counts = {"new": 0, "changed": 0, "reactivated": 0, "inactive": 0, "skipped": 0, "unchanged": 0}
    actions = []
    for rec in rows:
        m = existing.get(rec["code"])
        changes = []
        if upload_type == ADD:
            kind = "skipped" if m else "new"
        elif upload_type == CHANGE:
            if not m:
                kind = "new"
            else:
                changes = diff(m, rec)
                if m.status == Status.INACTIVE:
                    kind = "reactivated"
                    changes.append(("Status", "Inactive", "Active"))
                else:
                    kind = "changed" if changes else "unchanged"
        else:
            if not m:
                kind = "skipped"
            elif m.status == Status.ACTIVE:
                kind = "inactive"
                changes = [("Status", "Active", "Inactive")]
            else:
                kind = "unchanged"
        counts[kind] += 1
        actions.append({"kind": kind, "rec": rec, "changes": changes})
    return actions, counts


def create_preview(fileobj, filename, upload_type, user):
    rows, total, issues = validate(fileobj, upload_type)
    errors = sum(1 for i in issues if i["level"] == ERROR)
    actions, counts = plan(rows, upload_type) if not errors else ([], {})
    details = [{"kind": a["kind"], "code": a["rec"]["code"], "row": a["rec"]["row"],
                "changes": [f"{label}: {old if old is not None else ''} → {new if new is not None else ''}"
                            for label, old, new in a["changes"]]}
               for a in actions if a["kind"] != "unchanged"]
    return UploadBatch.objects.create(
        module=MODULE, upload_type=upload_type, source_filename=filename[:255], uploaded_by=user,
        state=UploadBatch.State.FAILED if errors else UploadBatch.State.PREVIEW,
        summary={"total": total, "valid": len(rows), **counts, "details": details},
        preview_rows=rows if not errors else [], issues=issues,
        error_count=errors, warning_count=sum(1 for i in issues if i["level"] == "Warning"),
    )


class ApplyRejected(Exception):
    pass


def apply(batch, user):
    """[반영]: 미리보기 내용 그대로 한 Transaction으로 저장. 호출자가 upload_lock 안에서 호출한다."""
    if batch.state != UploadBatch.State.PREVIEW:
        raise ApplyRejected("This upload cannot be applied (already applied, cancelled or has errors).")
    # 미리보기 이후 다른 사용자가 Material Master를 바꿨으면 거절 (설계/03 권장안 3)
    if Material.objects.filter(updated_at__gt=batch.created_at).exists():
        raise ApplyRejected("Material Master was changed by another user after this preview. Upload again. "
                            "(미리보기 이후 다른 사용자가 먼저 변경했습니다. 다시 Upload하세요.)")
    actions, _ = plan(batch.preview_rows, batch.upload_type)
    users = {u.username: u for u in User.objects.all()}
    now = timezone.now()
    with transaction.atomic():
        for a in actions:
            kind, rec = a["kind"], a["rec"]
            if kind in ("skipped", "unchanged"):
                continue
            if kind == "new":
                m = Material(material_code=rec["code"], created_by=user)
            else:
                m = Material.objects.select_related("purchaser").get(material_code=rec["code"])
            if kind == "inactive":
                m.status, m.inactive_at, m.inactive_by = Status.INACTIVE, now, user
                change_type = MaterialHistory.ChangeType.INACTIVE
            else:
                m.description, m.spec, m.vendor, m.country = rec["description"], rec["spec"], rec["vendor"], rec["country"]
                m.unit_id, m.lead_time_weeks = rec["unit"], rec["lead_time_weeks"]
                m.purchaser = users.get(rec["purchaser"]) if rec["purchaser"] else None
                m.status = Status.ACTIVE
                change_type = {"new": MaterialHistory.ChangeType.ADD, "changed": MaterialHistory.ChangeType.CHANGE,
                               "reactivated": MaterialHistory.ChangeType.REACTIVATE}[kind]
            m.updated_at, m.updated_by = now, user
            if m.pk:
                m.version += 1
            m.save()
            MaterialHistory.record(m, change_type, user, now, batch)
        batch.state, batch.applied_at = UploadBatch.State.APPLIED, now
        batch.save(update_fields=["state", "applied_at"])
        if any(a["kind"] not in ("skipped", "unchanged") for a in actions):
            SystemStatus.mark_data_changed()


def _parse_screen_row(post, pk, units, users):
    """화면 수정 값 검증 → (값 dict, 오류 목록)."""
    errors = []
    unit = (post.get(f"unit_{pk}") or "").strip().upper()
    if unit not in units:
        errors.append("Unit is required and must be an allowed value.")
    purchaser = (post.get(f"purchaser_{pk}") or "").strip().lower() or None
    if purchaser and purchaser not in users:
        errors.append("Purchaser is not a registered user.")
    try:
        lt = to_int(post.get(f"lt_{pk}"))
        if lt is None or lt < 1:
            errors.append("L/T(Weeks) must be a whole number of 1 or more.")
    except ValueError:
        lt = None
        errors.append("L/T(Weeks) must be a whole number of 1 or more.")
    status = post.get(f"status_{pk}")
    if status not in Status.values:
        errors.append("Invalid Status.")
    values = {"description": to_text(post.get(f"desc_{pk}")), "spec": to_text(post.get(f"spec_{pk}")),
              "unit": unit, "purchaser": purchaser, "vendor": to_text(post.get(f"vendor_{pk}")),
              "country": to_text(post.get(f"country_{pk}")), "lead_time_weeks": lt}
    return values, status, errors


def save_rows(post, user):
    """화면 Save: 선택된 행만 저장 (Ⅵ-1-9-1). 결과 메시지 목록 [(level, text)]."""
    ids = [int(x) for x in post.getlist("sel") if x.isdigit()]
    if not ids:
        return [("error", "Select rows first.")]
    units = set(UnitCode.objects.values_list("code", flat=True))
    users = {u.username: u for u in User.objects.all()}
    msgs, saved = [], 0
    now = timezone.now()
    for pk in ids:
        with transaction.atomic():
            m = Material.objects.select_for_update(of=("self",)).select_related("purchaser").filter(pk=pk).first()
            if m is None:
                continue
            version = post.get(f"version_{pk}", "")
            if not version.isdigit() or int(version) != m.version:
                msgs.append(("error", f"{m.material_code}: Another user changed this data first. "
                                      "The latest data has been reloaded. (다른 사용자가 먼저 수정했습니다. "
                                      "최신 Data를 다시 조회합니다.)"))
                continue
            values, status, errors = _parse_screen_row(post, pk, units, users)
            if errors:
                msgs.append(("error", f"{m.material_code}: " + " ".join(errors)))
                continue
            changed = bool(diff(m, values))
            if not changed and status == m.status:
                continue
            m.description, m.spec, m.vendor, m.country = (values["description"], values["spec"],
                                                          values["vendor"], values["country"])
            m.unit_id, m.lead_time_weeks = values["unit"], values["lead_time_weeks"]
            m.purchaser = users.get(values["purchaser"]) if values["purchaser"] else None
            change_type = MaterialHistory.ChangeType.SCREEN
            if status != m.status:
                if status == Status.INACTIVE:
                    m.inactive_at, m.inactive_by = now, user
                    change_type = MaterialHistory.ChangeType.INACTIVE
                else:
                    change_type = MaterialHistory.ChangeType.REACTIVATE
                m.status = status
            m.updated_at, m.updated_by, m.version = now, user, m.version + 1
            m.save()
            MaterialHistory.record(m, change_type, user, now)
            saved += 1
    if saved:
        SystemStatus.mark_data_changed()
        msgs.append(("success", f"{saved} row(s) saved."))
    elif not msgs:
        msgs.append(("info", "No changes to save."))
    return msgs
