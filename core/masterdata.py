"""Master Data(Module 1 Material Master, Module 2 Assy Master) 공통 처리.

각 Module은 MasterSpec(어떤 Column이 있고 어떻게 검사하는지)만 정의하고,
Upload 검증 → 미리보기 분류 → 반영, 화면 Save, History 기록은 여기서 공통으로 처리한다.
(Ⅵ-1, Ⅵ-2: 두 Module의 규칙이 같으므로 한 곳에서 관리)
"""
from dataclasses import dataclass
from typing import Callable

from django.db import transaction
from django.utils import timezone

from .excel import ERROR, INFO, issue, read_sheet, to_code, to_text
from .models import Status, SystemStatus, UploadBatch

ADD, CHANGE, INACTIVE = "ADD", "CHANGE", "INACTIVE"
UPLOAD_TYPES = {ADD: "Add", CHANGE: "Change", INACTIVE: "Inactive"}
MSG_CONFLICT = ("Another user changed this data first. The latest data has been reloaded. "
                "(다른 사용자가 먼저 수정했습니다. 최신 Data를 다시 조회합니다.)")


def parse_text(raw, ctx):
    return to_text(raw)


def parse_code_attr(raw, ctx):
    """Key가 아닌 Code 속성(예: Assy Code)도 같은 정규화 적용 (Ⅵ-2-4-0)."""
    return to_code(raw)


@dataclass
class Field:
    name: str                       # 모델 속성 = 미리보기 행(dict)의 키
    header: str                     # Excel Header
    label: str                      # 화면·변경내역 표시 이름
    form: str                       # 화면 입력칸 이름 접두어
    parse: Callable = parse_text    # (원래 값, ctx) -> 정규화 값. 잘못되면 ValueError(사유)
    get: Callable = None            # (obj) -> 비교용 값. 기본: getattr
    set: Callable = None            # (obj, 값, ctx). 기본: setattr


@dataclass
class MasterSpec:
    module: str                     # 예: M1
    sheet: str                      # Upload 시트명
    code_header: str                # Key Column Header
    code_field: str                 # Key 모델 속성
    model: type
    history: type                   # classmethod record(obj, change_type, user, when, batch) 필요
    fields: list
    required: list                  # Add/Change에서 필수 Header (Key 제외)
    banned_codes: frozenset = frozenset()
    select_related: tuple = ()
    context: Callable = dict        # 검증에 필요한 참조값 (허용 Unit, 사용자 목록 등)

    @property
    def upload_headers(self):
        return [self.code_header] + [f.header for f in self.fields]

    def value(self, obj, f):
        return f.get(obj) if f.get else getattr(obj, f.name)

    def assign(self, obj, f, v, ctx):
        f.set(obj, v, ctx) if f.set else setattr(obj, f.name, v)

    def diff(self, obj, rec):
        """바뀐 필드 [(이름, 이전, 이후)]."""
        return [(f.label, self.value(obj, f), rec[f.name]) for f in self.fields if self.value(obj, f) != rec[f.name]]

    def objects(self):
        return self.model.objects.select_related(*self.select_related)


# ---------- Upload ----------

def validate(spec, fileobj, upload_type):
    """Excel 읽기 + 업무 검증. (통과 행 목록, 읽은 행 수, issues)"""
    required = [spec.code_header] if upload_type == INACTIVE else [spec.code_header] + spec.required
    optional = [h for h in spec.upload_headers if h not in required]
    raw_rows, issues = read_sheet(fileobj, spec.sheet, required, optional)
    if upload_type == INACTIVE and raw_rows:
        issues.append(issue(INFO, spec.sheet, "", "", f"Inactive upload: only '{spec.code_header}' is used."))
    ctx = spec.context()
    seen, rows = {}, []
    for raw in raw_rows:
        n = raw["_row"]
        try:
            code = to_code(raw.get(spec.code_header))
        except ValueError as e:
            issues.append(issue(ERROR, spec.sheet, n, spec.code_header, str(e), str(raw.get(spec.code_header))))
            continue
        if not code:
            issues.append(issue(ERROR, spec.sheet, n, spec.code_header, f"{spec.code_header} is required."))
            continue
        if code in spec.banned_codes:
            issues.append(issue(ERROR, spec.sheet, n, spec.code_header,
                                f"'{code}' cannot be used as a {spec.code_header}.", code))
            continue
        if code in seen:
            issues.append(issue(ERROR, spec.sheet, n, spec.code_header,
                                f"Duplicate {spec.code_header} (also in row {seen[code]}). "
                                "Fix the Excel file and upload again.", code))
            continue
        seen[code] = n
        rec = {"row": n, "code": code}
        if upload_type != INACTIVE:
            errors = []
            for f in spec.fields:
                try:
                    rec[f.name] = f.parse(raw.get(f.header), ctx)
                except ValueError as e:
                    errors.append(issue(ERROR, spec.sheet, n, f.header, str(e), code))
            if errors:
                issues.extend(errors)
                continue
        rows.append(rec)
    return rows, len(raw_rows), issues


def plan(spec, rows, upload_type):
    """DB 현재값과 비교해 각 행의 처리 방법을 정한다. (actions, counts)"""
    existing = {getattr(o, spec.code_field): o for o in
                spec.objects().filter(**{f"{spec.code_field}__in": [r["code"] for r in rows]})}
    counts = {"new": 0, "changed": 0, "reactivated": 0, "inactive": 0, "skipped": 0, "unchanged": 0}
    actions = []
    for rec in rows:
        obj = existing.get(rec["code"])
        changes = []
        if upload_type == ADD:
            kind = "skipped" if obj else "new"
        elif upload_type == CHANGE:
            if not obj:
                kind = "new"
            else:
                changes = spec.diff(obj, rec)
                if obj.status == Status.INACTIVE:
                    kind = "reactivated"
                    changes.append(("Status", "Inactive", "Active"))
                else:
                    kind = "changed" if changes else "unchanged"
        else:
            if not obj:
                kind = "skipped"
            elif obj.status == Status.ACTIVE:
                kind = "inactive"
                changes = [("Status", "Active", "Inactive")]
            else:
                kind = "unchanged"
        counts[kind] += 1
        actions.append({"kind": kind, "rec": rec, "changes": changes})
    return actions, counts


def _show(v):
    return "" if v is None else v


def create_preview(spec, fileobj, filename, upload_type, user):
    rows, total, issues = validate(spec, fileobj, upload_type)
    errors = sum(1 for i in issues if i["level"] == ERROR)
    actions, counts = plan(spec, rows, upload_type) if not errors else ([], {})
    details = [{"kind": a["kind"], "code": a["rec"]["code"], "row": a["rec"]["row"],
                "changes": [f"{label}: {_show(old)} → {_show(new)}" for label, old, new in a["changes"]]}
               for a in actions if a["kind"] != "unchanged"]
    return UploadBatch.objects.create(
        module=spec.module, upload_type=upload_type, source_filename=filename[:255], uploaded_by=user,
        state=UploadBatch.State.FAILED if errors else UploadBatch.State.PREVIEW,
        summary={"total": total, "valid": len(rows), **counts, "details": details},
        preview_rows=rows if not errors else [], issues=issues,
        error_count=errors, warning_count=sum(1 for i in issues if i["level"] == "Warning"),
    )


class ApplyRejected(Exception):
    pass


def apply(spec, batch, user):
    """[반영]: 미리보기 내용 그대로 한 Transaction으로 저장. 호출자가 upload_lock 안에서 호출한다."""
    if batch.state != UploadBatch.State.PREVIEW:
        raise ApplyRejected("This upload cannot be applied (already applied, cancelled or has errors).")
    if spec.model.objects.filter(updated_at__gt=batch.created_at).exists():
        raise ApplyRejected("Data was changed by another user after this preview. Upload again. "
                            "(미리보기 이후 다른 사용자가 먼저 변경했습니다. 다시 Upload하세요.)")
    actions, _ = plan(spec, batch.preview_rows, batch.upload_type)
    ctx = spec.context()
    now = timezone.now()
    kinds = {"new": "Add", "changed": "Change", "reactivated": "Reactivate", "inactive": "Inactive"}
    with transaction.atomic():
        for a in actions:
            kind, rec = a["kind"], a["rec"]
            if kind not in kinds:
                continue
            if kind == "new":
                obj = spec.model(**{spec.code_field: rec["code"]}, created_by=user)
            else:
                obj = spec.objects().get(**{spec.code_field: rec["code"]})
            if kind == "inactive":
                obj.status, obj.inactive_at, obj.inactive_by = Status.INACTIVE, now, user
            else:
                for f in spec.fields:
                    spec.assign(obj, f, rec[f.name], ctx)
                obj.status = Status.ACTIVE
            obj.updated_at, obj.updated_by = now, user
            if obj.pk:
                obj.version += 1
            obj.save()
            spec.history.record(obj, kinds[kind], user, now, batch)
        batch.state, batch.applied_at = UploadBatch.State.APPLIED, now
        batch.save(update_fields=["state", "applied_at"])
        if any(a["kind"] in kinds for a in actions):
            SystemStatus.mark_data_changed()


# ---------- 화면 수정 ----------

def save_rows(spec, post, user):
    """화면 Save: 체크된 행만 저장, Optimistic Lock (Ⅵ-1-9-1, Ⅰ-11). 결과 메시지 [(level, text)]."""
    ids = [int(x) for x in post.getlist("sel") if x.isdigit()]
    if not ids:
        return [("error", "Select rows first.")]
    ctx = spec.context()
    msgs, saved = [], 0
    now = timezone.now()
    for pk in ids:
        with transaction.atomic():
            obj = spec.objects().select_for_update(of=("self",)).filter(pk=pk).first()
            if obj is None:
                continue
            code = getattr(obj, spec.code_field)
            version = post.get(f"version_{pk}", "")
            if not version.isdigit() or int(version) != obj.version:
                msgs.append(("error", f"{code}: {MSG_CONFLICT}"))
                continue
            values, errors = {}, []
            for f in spec.fields:
                try:
                    values[f.name] = f.parse(post.get(f"{f.form}_{pk}"), ctx)
                except ValueError as e:
                    errors.append(str(e))
            status = post.get(f"status_{pk}")
            if status not in Status.values:
                errors.append("Invalid Status.")
            if errors:
                msgs.append(("error", f"{code}: " + " ".join(errors)))
                continue
            if not spec.diff(obj, values) and status == obj.status:
                continue
            for f in spec.fields:
                spec.assign(obj, f, values[f.name], ctx)
            change_type = "Screen"
            if status != obj.status:
                if status == Status.INACTIVE:
                    obj.inactive_at, obj.inactive_by = now, user
                    change_type = "Inactive"
                else:
                    change_type = "Reactivate"
                obj.status = status
            obj.updated_at, obj.updated_by, obj.version = now, user, obj.version + 1
            obj.save()
            spec.history.record(obj, change_type, user, now)
            saved += 1
    if saved:
        SystemStatus.mark_data_changed()
        msgs.append(("success", f"{saved} row(s) saved."))
    elif not msgs:
        msgs.append(("info", "No changes to save."))
    return msgs
