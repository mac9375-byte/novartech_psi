"""Master Data 화면 공통 (조회·Save·Upload 미리보기/반영/취소·Download·History·Template·검증결과)."""
from dataclasses import dataclass
from typing import Callable

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path, reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.permissions import has_perm, require

from . import masterdata as md
from .context import module_context
from .excel import xlsx_response
from .locks import UploadBusy, upload_lock
from .models import Status, UploadBatch

STATUS_FILTERS = [("ACTIVE", "Active"), ("ALL", "All"), ("INACTIVE", "Inactive")]
COUNT_LABELS = [("new", "New (신규등록)"), ("changed", "Changed (수정)"), ("inactive", "Inactive"),
                ("skipped", "Skipped (무시)"), ("reactivated", "Reactivated (재활성화)"),
                ("unchanged", "No change (변경 없음)")]


def stamp(dt):
    """Download·History 시각: yyyy-mm-dd hh:mm (사용자 Timezone)."""
    return timezone.localtime(dt).strftime("%Y-%m-%d %H:%M") if dt else ""


@dataclass
class MasterScreen:
    spec: md.MasterSpec
    ns: str                         # URL namespace (예: materials)
    title: str                      # 화면 이름 (예: Material Master)
    file_prefix: str                # Download 파일명 접두어 (예: MaterialMaster)
    template: str                   # 목록 화면 템플릿
    search_fields: list             # [(key, 라벨, [조회 경로])], 첫 항목이 기본
    download_headers: list
    download_row: Callable          # (no, obj) -> tuple
    history_row: Callable           # (no, history) -> tuple (download_headers 순서 + 변경 구분, 변경자)
    extra_context: Callable = lambda request: {}

    # ----- 조회 조건 -----
    def filters(self, params):
        status = params.get("status", "ACTIVE")
        status = status if status in dict(STATUS_FILTERS) else "ACTIVE"
        keys = [f[0] for f in self.search_fields]
        fld = params.get("field", keys[0])
        fld = fld if fld in keys else keys[0]
        return status, fld, (params.get("q") or "").strip()

    def queryset(self, params):
        """Status + 검색조건 + 검색어 (부분일치, 대소문자 무시)."""
        status, fld, q = self.filters(params)
        qs = self.spec.objects()
        if status != "ALL":
            qs = qs.filter(status=status)
        if q:
            cond = Q()
            for lookup in {f[0]: f[2] for f in self.search_fields}[fld]:
                cond |= Q(**{f"{lookup}__icontains": q})
            qs = qs.filter(cond)
        return qs.order_by(self.spec.code_field)

    def back(self, request):
        q = request.POST.get("return_qs", "")
        return redirect(reverse(f"{self.ns}:list") + (f"?{q}" if q else ""))

    def batch(self, pk):
        return get_object_or_404(UploadBatch, pk=pk, module=self.spec.module)

    # ----- 화면 -----
    def list_view(self, request):
        status, fld, q = self.filters(request.GET)
        qs = request.GET.urlencode()
        urls = {k: reverse(f"{self.ns}:{k}") for k in ("save", "upload", "download", "history", "template")}
        return render(request, self.template, module_context(
            self.spec.module, rows=self.queryset(request.GET), status=status, field=fld, q=q,
            status_filters=STATUS_FILTERS, search_fields=[(f[0], f[1]) for f in self.search_fields],
            statuses=Status.choices, can_edit=has_perm(request.user, "edit"),
            can_upload=has_perm(request.user, "upload"), query_string=qs, urls=urls,
            sheet=self.spec.sheet, **self.extra_context(request),
        ))

    def save_view(self, request):
        for level, text in md.save_rows(self.spec, request.POST, request.user):
            getattr(messages, level)(request, text)
        return self.back(request)

    def upload_view(self, request):
        upload_type, f = request.POST.get("upload_type"), request.FILES.get("file")
        if upload_type not in md.UPLOAD_TYPES:
            messages.error(request, "Select an Upload Type.")
            return self.back(request)
        if not f or not f.name.lower().endswith(".xlsx"):
            messages.error(request, "Select an Excel (.xlsx) file.")
            return self.back(request)
        try:
            with upload_lock(self.spec.module):
                batch = md.create_preview(self.spec, f, f.name, upload_type, request.user)
        except UploadBusy as e:
            messages.error(request, str(e))
            return self.back(request)
        return redirect(f"{self.ns}:preview", batch.pk)

    def preview_view(self, request, pk):
        batch = self.batch(pk)
        return render(request, "core/upload_preview.html", module_context(
            self.spec.module, batch=batch, title=self.title,
            upload_type_label=md.UPLOAD_TYPES.get(batch.upload_type, ""),
            counts=[(label, batch.summary.get(key, 0)) for key, label in COUNT_LABELS],
            apply_url=reverse(f"{self.ns}:apply", args=[pk]), cancel_url=reverse(f"{self.ns}:cancel", args=[pk]),
            back_url=reverse(f"{self.ns}:list"), issues_url=reverse(f"{self.ns}:issues", args=[pk]),
        ))

    def apply_view(self, request, pk):
        batch = self.batch(pk)
        try:
            with upload_lock(self.spec.module):
                md.apply(self.spec, batch, request.user)
        except (UploadBusy, md.ApplyRejected) as e:
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

    def download_view(self, request):
        rows = [self.download_row(n, o) for n, o in enumerate(self.queryset(request.GET), start=1)]
        return xlsx_response(f"{self.file_prefix}_{timezone.localtime():%Y%m%d_%H%M}.xlsx", self.spec.sheet,
                             self.download_headers, rows, self.spec.upload_headers)

    def history_view(self, request):
        codes = list(self.queryset(request.GET).values_list(self.spec.code_field, flat=True))
        hist = self.spec.history.objects.filter(**{f"{self.spec.code_field}__in": codes}).select_related("changed_by")
        rows = [self.history_row(n, h) for n, h in enumerate(hist, start=1)]
        return xlsx_response(f"{self.file_prefix}_History_{timezone.localtime():%Y%m%d_%H%M}.xlsx", "History",
                             self.download_headers + ["Change Type", "Changed By"], rows)

    def template_view(self, request):
        return xlsx_response(f"{self.spec.sheet}_Template.xlsx", self.spec.sheet, self.spec.upload_headers, [],
                             self.spec.upload_headers)

    def urls(self):
        up, ed = require("upload"), require("edit")
        return [
            path("", self.list_view, name="list"),
            path("save/", require_POST(ed(self.save_view)), name="save"),
            path("upload/", require_POST(up(self.upload_view)), name="upload"),
            path("upload/<int:pk>/", up(self.preview_view), name="preview"),
            path("upload/<int:pk>/apply/", require_POST(up(self.apply_view)), name="apply"),
            path("upload/<int:pk>/cancel/", require_POST(up(self.cancel_view)), name="cancel"),
            path("upload/<int:pk>/issues.xlsx", up(self.issues_view), name="issues"),
            path("download.xlsx", self.download_view, name="download"),
            path("history.xlsx", self.history_view, name="history"),
            path("template.xlsx", up(self.template_view), name="template"),
        ]
