from django.urls import path, reverse
from django.utils import timezone

from accounts.permissions import has_perm
from core import lookup
from core.excel import xlsx_response
from core.fmt import frac
from core.masterviews import stamp
from core.tablepage import cell, render_table
from core.uploadflow import UploadFlow

from . import services as svc
from .models import BomVersion

STATUSES = [("ACTIVE", "Active"), ("ALL", "All"), ("INACTIVE", "Inactive"), ("NODB", "No DB")]
FIELDS = [("cust", "Cust. Code"), ("mat", "Mat. Code")]
COLUMNS = [("No", "sys"), ("Cust. Code", "up"), ("Mat. Code", "up"), ("Desc.", "sys"), ("Spec.", "sys"),
           ("Unit", "up"), ("Q'ty", "up"), ("Type", "sys"), ("Model", "sys"), ("Item", "sys"),
           ("Update", "sys"), ("Status", "sys")]
DL_HEADERS = ["Customer Code", "Material Code", "Desc.", "Spec.", "Unit", "Q'ty", "Type", "Model", "Item",
              "Update", "Status"]


def _filters(params):
    status = params.get("status", "ACTIVE")
    status = status if status in dict(STATUSES) else "ACTIVE"
    field = params.get("field", "cust")
    field = field if field in dict(FIELDS) else "cust"
    return status, field, (params.get("q") or "").strip().upper()


def _versions(params):
    """Assy Status + 검색조건 (Cust. Code는 해당 Assy, Mat. Code는 그 자재를 포함하는 Assy) (Ⅵ-3-10)."""
    status, field, q = _filters(params)
    qs = BomVersion.objects.filter(is_current=True)
    if q:
        qs = (qs.filter(customer_code__icontains=q) if field == "cust"
              else qs.filter(lines__material_code__icontains=q).distinct())
    versions = list(qs.order_by("customer_code").prefetch_related("lines"))
    assies = lookup.assies([v.customer_code for v in versions])
    want = {"ACTIVE": "Active", "INACTIVE": "Inactive", "NODB": lookup.NO_DB}.get(status)
    out = [(v, assies.get(v.customer_code)) for v in versions]
    return [(v, a) for v, a in out if want is None or lookup.status(a) == want]


def _rows(params):
    """화면/Download 공통 행: Assy 행 + 자재 행 (Desc·Spec·Type·Model·Item은 최신 Master 값, 계층 2)."""
    pairs = _versions(params)
    mats = lookup.materials({l.material_code for v, _ in pairs for l in v.lines.all()})
    out = []
    for v, a in pairs:
        st = lookup.status(a)
        tmi = (a.assy_type, a.model_name, a.item) if a else (None, None, None)
        out.append(("assy", v, [v.customer_code, "Assy", None, None, None, None, *tmi], st))
        for l in v.lines.all():
            m = mats.get(l.material_code)
            out.append(("line", v, [v.customer_code, l.material_code, m.description if m else None,
                                    m.spec if m else None, l.unit, l.qty, *tmi], lookup.status(m)))
    return out


def bom_list(request):
    status, field, q = _filters(request.GET)
    rows = []
    for n, (kind, v, vals, st) in enumerate(_rows(request.GET), start=1):
        vals = list(vals)
        vals[5] = frac(vals[5]) if kind == "line" else ""
        rows.append({"cls": "agg blockstart" if kind == "assy" else "",
                     "cells": [cell(n)] + [cell(x) for x in vals]
                              + [cell(timezone.localtime(v.updated_at).strftime("%Y-%m-%d")),
                                 cell(st, lookup.status_cls(st))]})
    can_up = has_perm(request.user, "upload")
    qs = request.GET.urlencode()
    return render_table(
        request, "M3", "BOM", COLUMNS, rows,
        controls={"statuses": STATUSES, "status": status, "fields": FIELDS, "field": field, "q": q},
        buttons=[{"kind": "upload", "label": "Upload", "disabled": not can_up},
                 {"label": "Download", "href": reverse("bom:download") + "?" + qs},
                 {"label": "History", "href": reverse("bom:history") + "?" + qs}],
        upload={"action": reverse("bom:upload"), "types": list(svc.UPLOAD_TYPES.items()),
                "note": "Sheet: BOM · Columns: Customer Code / Material Code / Unit / Q'ty. "
                        "Each Assy starts with a row whose Material Code is Assy."} if can_up else None,
    )


def bom_download(request):
    data = [[*vals[:5], "" if kind == "assy" else _qty_text(vals[5]), *vals[6:], stamp(v.updated_at), st]
            for kind, v, vals, st in _rows(request.GET)]
    return xlsx_response("BOM_" + _now() + ".xlsx", svc.SHEET, DL_HEADERS, data,
                         [svc.H_CUST, svc.H_MAT, svc.H_UNIT, svc.H_QTY])


def _qty_text(f):
    """Download 값: 분수 문자열 그대로 (재Upload 가능하도록 쉼표 없음)."""
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def _now():
    return f"{timezone.localtime():%Y%m%d_%H%M}"


def bom_history(request):
    """검색 결과 Assy의 모든 BOM 버전(현재 포함)을 Update 순으로. 이력 행은 등록 시점 값 (F-8)."""
    codes = [v.customer_code for v, _ in _versions(request.GET)]
    data = []
    for v in BomVersion.objects.filter(customer_code__in=codes).prefetch_related("lines").select_related("updated_by"):
        tmi = [v.assy_type, v.model_name, v.item]
        state = "Current" if v.is_current else "History"
        data.append([v.customer_code, "Assy", None, None, None, None, *tmi, stamp(v.updated_at), state,
                     v.updated_by.username])
        for l in v.lines.all():
            data.append([v.customer_code, l.material_code, l.desc_snap, l.spec_snap, l.unit, _qty_text(l.qty), *tmi,
                         stamp(v.updated_at), state, v.updated_by.username])
    return xlsx_response("BOM_History_" + _now() + ".xlsx", "History",
                         DL_HEADERS[:-1] + ["Version", "Changed By"], data)


FLOW = UploadFlow(module=svc.MODULE, ns="bom", title="BOM", file_prefix="BOM", validate=svc.validate,
                  apply=svc.apply, count_labels=svc.COUNT_LABELS,
                  upload_types={k: v.split(":")[0] for k, v in svc.UPLOAD_TYPES.items()})

app_name = "bom"
urlpatterns = [
    path("", bom_list, name="list"),
    path("download.xlsx", bom_download, name="download"),
    path("history.xlsx", bom_history, name="history"),
    *FLOW.urls(),
]
