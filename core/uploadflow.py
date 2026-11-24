"""Module 3~8 Excel Upload 공통 흐름: Upload → 검증 결과(미리보기) → [반영] / 취소 (Ⅳ-5).

각 Module은 validate()와 apply()만 정의한다.
- validate(fileobj, upload_type, week) -> (rows, total, issues, counts, details)
- apply(batch, user): batch.preview_rows를 한 Transaction 안에서 저장
"""
from dataclasses import dataclass
from typing import Callable

from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path, reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.permissions import require

from . import weeks
from .context import module_context
from .excel import ERROR, WARNING, xlsx_response
from .locks import UploadBusy, upload_lock
from .models import OperationLog, SystemStatus, UploadBatch


class ApplyRejected(Exception):
    pass


@dataclass
class UploadFlow:
    module: str
    ns: str
    title: str
    file_prefix: str
    validate: Callable
    apply: Callable
    count_labels: list
    upload_types: dict = None       # BOM: {"ADD": "Add", "CHANGE": "Change"}
    weekly: bool = False            # Module 5~8: 작업 주차(Current Week) 데이터만 교체
    depends: tuple = ()             # 미리보기 후 이 Module이 반영되면 다시 Upload (예: Open PO ↔ Scheduled Receipt)

    def lock_key(self, week):
        return f"{self.module}:{week}"

    def back(self, request):
        q = request.POST.get("return_qs", "")
        return redirect(reverse(f"{self.ns}:list") + (f"?{q}" if q else ""))

    def batch(self, pk):
        return get_object_or_404(UploadBatch, pk=pk, module=self.module)

    def upload_view(self, request):
        upload_type, f = request.POST.get("upload_type", ""), request.FILES.get("file")
        if self.upload_types and upload_type not in self.upload_types:
            messages.error(request, "Select an Upload Type.")
            return self.back(request)
        if not f or not f.name.lower().endswith(".xlsx"):
            messages.error(request, "Select an Excel (.xlsx) file.")
            return self.back(request)
        week = weeks.current_week() if self.weekly else ""  # 과거 주차 Upload 불가 (Ⅳ-5)
        try:
            with upload_lock(self.lock_key(week)):
                rows, total, issues, counts, details = self.validate(f, upload_type, week)
                errors = sum(1 for i in issues if i["level"] == ERROR)
                batch = UploadBatch.objects.create(
                    module=self.module, week=week, upload_type=upload_type, source_filename=f.name[:255],
                    uploaded_by=request.user,
                    state=UploadBatch.State.FAILED if errors else UploadBatch.State.PREVIEW,
                    summary={"total": total, "valid": len(rows), **counts, "details": details},
                    preview_rows=rows if not errors else [], issues=issues, error_count=errors,
                    warning_count=sum(1 for i in issues if i["level"] == WARNING),
                )
        except UploadBusy as e:
            messages.error(request, str(e))
            return self.back(request)
        return redirect(f"{self.ns}:preview", batch.pk)

    def preview_view(self, request, pk):
        batch = self.batch(pk)
        return render(request, "core/upload_preview.html", module_context(
            self.module, batch=batch, title=self.title + (f" · {batch.week}" if batch.week else ""),
            upload_type_label=(self.upload_types or {}).get(batch.upload_type, "Replace (전체교체)"),
            counts=[(label, batch.summary.get(key, 0)) for key, label in self.count_labels],
            apply_url=reverse(f"{self.ns}:apply", args=[pk]), cancel_url=reverse(f"{self.ns}:cancel", args=[pk]),
            back_url=reverse(f"{self.ns}:list"), issues_url=reverse(f"{self.ns}:issues", args=[pk]),
        ))

    def _check(self, batch):
        if batch.state != UploadBatch.State.PREVIEW:
            raise ApplyRejected("This upload cannot be applied (already applied, cancelled or has errors).")
        if self.weekly and batch.week != weeks.current_week():
            raise ApplyRejected("The working week has changed since this preview. Upload again.")
        newer = UploadBatch.objects.filter(module__in=(self.module, *self.depends), week=batch.week,
                                           state=UploadBatch.State.APPLIED, applied_at__gt=batch.created_at)
        reset = self.weekly and OperationLog.objects.filter(kind=OperationLog.Kind.RESET, week=batch.week,
                                                            success=True, at__gt=batch.created_at).exists()
        if newer.exists() or reset:
            raise ApplyRejected("Data was changed after this preview. Upload again. "
                                "(미리보기 이후 데이터가 변경되었습니다. 다시 Upload하세요.)")

    def apply_view(self, request, pk):
        batch = self.batch(pk)
        try:
            with upload_lock(self.lock_key(batch.week)):
                self._check(batch)
                with transaction.atomic():
                    self.apply(batch, request.user)
                    batch.state, batch.applied_at = UploadBatch.State.APPLIED, timezone.now()
                    batch.save(update_fields=["state", "applied_at"])
                    SystemStatus.mark_data_changed()
        except (UploadBusy, ApplyRejected) as e:
            messages.error(request, str(e))
            return redirect(f"{self.ns}:preview", pk)
        messages.success(request, "Upload applied.")
        return redirect(f"{self.ns}:list")

    def cancel_view(self, request, pk):
        batch = self.batch(pk)
        if batch.state == UploadBatch.State.PREVIEW:
            batch.state = UploadBatch.State.CANCELLED
            batch.save(update_fields=["state"])
        messages.info(request, "Upload cancelled.")
        return redirect(f"{self.ns}:list")

    def issues_view(self, request, pk):
        batch = self.batch(pk)
        rows = [(i["level"], i["sheet"], i["row"], i["code"], i["field"], i["reason"]) for i in batch.issues]
        return xlsx_response(f"{self.file_prefix}_Validation_{batch.pk}.xlsx", "Validation",
                             ["Level", "Sheet", "Excel Row", "Code", "Field", "Reason"], rows)

    def urls(self):
        up = require("upload")
        return [
            path("upload/", require_POST(up(self.upload_view)), name="upload"),
            path("upload/<int:pk>/", up(self.preview_view), name="preview"),
            path("upload/<int:pk>/apply/", require_POST(up(self.apply_view)), name="apply"),
            path("upload/<int:pk>/cancel/", require_POST(up(self.cancel_view)), name="cancel"),
            path("upload/<int:pk>/issues.xlsx", up(self.issues_view), name="issues"),
        ]
