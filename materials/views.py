from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.models import IdStatus, User
from accounts.permissions import has_perm, require
from core.context import module_context
from core.excel import xlsx_response
from core.locks import UploadBusy, upload_lock
from core.models import UploadBatch

from . import services as svc
from .models import Material, MaterialHistory, Status, UnitCode

SEARCH_FIELDS = [
    ("code", "Mat. Code", ["material_code"]),
    ("desc", "Desc.", ["description"]),
    ("purchaser", "Purchaser", ["purchaser__name", "purchaser__username"]),
    ("vendor", "Vendor", ["vendor"]),
    ("country", "Country", ["country"]),
]
STATUS_FILTERS = [("ACTIVE", "Active"), ("ALL", "All"), ("INACTIVE", "Inactive")]
DOWNLOAD_HEADERS = ["No", "Material Code", "Desc.", "Spec.", "Unit", "Purchaser ID", "Purchaser",
                    "Vendor", "Country", "L/T(Weeks)", "Update", "Status"]


def _filters(params):
    status = params.get("status", "ACTIVE")
    status = status if status in dict(STATUS_FILTERS) else "ACTIVE"
    field = params.get("field", "code")
    field = field if field in [f[0] for f in SEARCH_FIELDS] else "code"
    return status, field, (params.get("q") or "").strip()


def _queryset(params):
    """Status + 검색조건 + 검색어 (부분일치, 대소문자 무시, Ⅵ-1-11·12)."""
    status, field, q = _filters(params)
    qs = Material.objects.select_related("purchaser")
    if status != "ALL":
        qs = qs.filter(status=status)
    if q:
        cond = Q()
        for lookup in dict((f[0], f[2]) for f in SEARCH_FIELDS)[field]:
            cond |= Q(**{f"{lookup}__icontains": q})
        qs = qs.filter(cond)
    return qs.order_by("material_code")


def _stamp(dt):
    return timezone.localtime(dt).strftime("%Y-%m-%d %H:%M") if dt else ""


def _back(request):
    q = request.POST.get("return_qs", "")
    return redirect(reverse("materials:list") + (f"?{q}" if q else ""))


def material_list(request):
    status, field, q = _filters(request.GET)
    return render(request, "materials/list.html", module_context(
        "M1",
        rows=_queryset(request.GET),
        status=status, field=field, q=q,
        status_filters=STATUS_FILTERS, search_fields=[(f[0], f[1]) for f in SEARCH_FIELDS],
        units=UnitCode.objects.all(),
        users=User.objects.order_by("name", "username"),
        approved=IdStatus.APPROVED,
        statuses=Status.choices,
        can_edit=has_perm(request.user, "edit"),
        can_upload=has_perm(request.user, "upload"),
        upload_types=svc.UPLOAD_TYPES,
        query_string=request.GET.urlencode(),
    ))


@require_POST
@require("edit")
def material_save(request):
    for level, text in svc.save_rows(request.POST, request.user):
        getattr(messages, level)(request, text)
    return _back(request)


@require_POST
@require("upload")
def material_upload(request):
    upload_type = request.POST.get("upload_type")
    f = request.FILES.get("file")
    if upload_type not in svc.UPLOAD_TYPES:
        messages.error(request, "Select an Upload Type.")
        return _back(request)
    if not f or not f.name.lower().endswith(".xlsx"):
        messages.error(request, "Select an Excel (.xlsx) file.")
        return _back(request)
    try:
        with upload_lock(svc.MODULE):
            batch = svc.create_preview(f, f.name, upload_type, request.user)
    except UploadBusy as e:
        messages.error(request, str(e))
        return _back(request)
    return redirect("materials:preview", batch.pk)


def _batch(pk):
    return get_object_or_404(UploadBatch, pk=pk, module=svc.MODULE)


@require("upload")
def material_preview(request, pk):
    batch = _batch(pk)
    return render(request, "core/upload_preview.html", module_context(
        "M1", batch=batch, title="Material Master", upload_type_label=svc.UPLOAD_TYPES.get(batch.upload_type, ""),
        counts=[(label, batch.summary.get(key, 0)) for key, label in [
            ("new", "New (신규등록)"), ("changed", "Changed (수정)"), ("inactive", "Inactive"),
            ("skipped", "Skipped (무시)"), ("reactivated", "Reactivated (재활성화)"),
            ("unchanged", "No change (변경 없음)")]],
        apply_url=reverse("materials:apply", args=[pk]), cancel_url=reverse("materials:cancel", args=[pk]),
        back_url=reverse("materials:list"), issues_url=reverse("materials:issues", args=[pk]),
    ))


@require_POST
@require("upload")
def material_apply(request, pk):
    batch = _batch(pk)
    try:
        with upload_lock(svc.MODULE):
            svc.apply(batch, request.user)
    except (UploadBusy, svc.ApplyRejected) as e:
        messages.error(request, str(e))
        return redirect("materials:preview", pk)
    messages.success(request, "Upload applied.")
    return redirect("materials:list")


@require_POST
@require("upload")
def material_cancel(request, pk):
    batch = _batch(pk)
    if batch.state == UploadBatch.State.PREVIEW:
        batch.state = UploadBatch.State.CANCELLED
        batch.save(update_fields=["state"])
    messages.info(request, "Upload cancelled.")
    return redirect("materials:list")


@require("upload")
def material_issues(request, pk):
    """검증 결과 Excel Download (권장안 5)."""
    batch = _batch(pk)
    rows = [(i["level"], i["sheet"], i["row"], i["code"], i["field"], i["reason"]) for i in batch.issues]
    return xlsx_response(f"MaterialMaster_Validation_{batch.pk}.xlsx", "Validation",
                         ["Level", "Sheet", "Excel Row", "Code", "Field", "Reason"], rows)


def material_download(request):
    rows = [(n, m.material_code, m.description, m.spec, m.unit_id,
             m.purchaser.username if m.purchaser else None, m.purchaser.name if m.purchaser else None,
             m.vendor, m.country, m.lead_time_weeks, _stamp(m.updated_at), m.get_status_display())
            for n, m in enumerate(_queryset(request.GET), start=1)]
    name = f"MaterialMaster_{timezone.localtime():%Y%m%d_%H%M}.xlsx"
    return xlsx_response(name, svc.SHEET, DOWNLOAD_HEADERS, rows, svc.UPLOAD_HEADERS)


def material_history(request):
    """현재 조회 결과 Code들의 전체 변경 이력 (Ⅵ-1-13-1, 권장안 2: 변경 구분·변경자 추가)."""
    codes = _queryset(request.GET).values_list("material_code", flat=True)
    hist = MaterialHistory.objects.filter(material_code__in=list(codes)).select_related("changed_by")
    rows = [(n, h.material_code, h.description, h.spec, h.unit, h.purchaser_id_text, h.purchaser_name,
             h.vendor, h.country, h.lead_time_weeks, _stamp(h.changed_at), h.status.title(),
             h.change_type, h.changed_by.username)
            for n, h in enumerate(hist, start=1)]
    name = f"MaterialMaster_History_{timezone.localtime():%Y%m%d_%H%M}.xlsx"
    return xlsx_response(name, "History", DOWNLOAD_HEADERS + ["Change Type", "Changed By"], rows)


@require("upload")
def material_template(request):
    """빈 Upload 양식 (권장안 4)."""
    return xlsx_response("MD_Material_Template.xlsx", svc.SHEET, svc.UPLOAD_HEADERS, [], svc.UPLOAD_HEADERS)
