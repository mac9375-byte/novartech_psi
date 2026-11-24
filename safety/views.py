from django.urls import path, reverse
from django.utils import timezone

from accounts.permissions import has_perm
from core import lookup
from core.excel import xlsx_response
from core.fmt import num
from core.masterviews import stamp
from core.tablepage import cell, render_table
from core.uploadflow import UploadFlow

from . import services as svc
from .models import SafetyHistory, SafetyStock

STATUSES = [("ACTIVE", "Active"), ("ALL", "All"), ("INACTIVE", "Inactive"), ("NODB", "No DB")]
FIELDS = [("cust", "Cust. Code"), ("assy", "Assy Code"), ("type", "Type")]
COLUMNS = [("No", "sys"), ("Cust. Code", "up"), ("Assy Code", "sys"), ("Type", "sys"), ("Model", "sys"),
           ("Item", "sys"), ("Customer", "sys"), ("Safety Q'ty", "up"), ("Update", "sys"), ("Status", "sys")]
DL_HEADERS = ["No", "Customer Code", "Assy Code", "Type", "Model", "Item", "Customer", "Safety Q'ty", "Update", "Status"]


def _data(params):
    status = params.get("status", "ACTIVE")
    status = status if status in dict(STATUSES) else "ACTIVE"
    field = params.get("field", "cust")
    field = field if field in dict(FIELDS) else "cust"
    q = (params.get("q") or "").strip().lower()
    rows = list(SafetyStock.objects.order_by("customer_code"))
    assies = lookup.assies([s.customer_code for s in rows])
    want = {"ACTIVE": "Active", "INACTIVE": "Inactive", "NODB": lookup.NO_DB}.get(status)
    out = []
    for s in rows:
        a = assies.get(s.customer_code)
        st = lookup.status(a)
        target = {"cust": s.customer_code, "assy": a.assy_code if a else "", "type": a.assy_type if a else ""}[field]
        if (want and st != want) or (q and q not in (target or "").lower()):
            continue
        out.append((s, a, st))
    return out, (status, field, q)


def safety_list(request):
    data, (status, field, q) = _data(request.GET)
    rows = [{"cells": [cell(n), cell(s.customer_code), cell(a and a.assy_code), cell(a and a.assy_type),
                       cell(a and a.model_name), cell(a and a.item), cell(a and a.customer),
                       cell(num(s.qty), "num"), cell(timezone.localtime(s.updated_at).strftime("%Y-%m-%d %H:%M")),
                       cell(st, lookup.status_cls(st))]}
            for n, (s, a, st) in enumerate(data, start=1)]
    can_up = has_perm(request.user, "upload")
    qs = request.GET.urlencode()
    return render_table(
        request, "M4", "Safety Stock", COLUMNS, rows,
        controls={"statuses": STATUSES, "status": status, "fields": FIELDS, "field": field, "q": q},
        buttons=[{"kind": "upload", "label": "Upload", "disabled": not can_up},
                 {"label": "Download", "href": reverse("safety:download") + "?" + qs},
                 {"label": "History", "href": reverse("safety:history") + "?" + qs}],
        upload={"action": reverse("safety:upload"),
                "note": "Sheet: SAFETY · Customer Code / Safety Q'ty. The whole Safety Stock list is replaced "
                        "by the file (전체교체)."} if can_up else None,
        banners=[("info", "Safety Q'ty is added to RTF week 14 (W+13) requirement only. "
                          "(RTF 14주차에만 합산, Prod. 미반영)")],
    )


def safety_download(request):
    data, _ = _data(request.GET)
    rows = [(n, s.customer_code, a and a.assy_code, a and a.assy_type, a and a.model_name, a and a.item,
             a and a.customer, s.qty, stamp(s.updated_at), st) for n, (s, a, st) in enumerate(data, start=1)]
    return xlsx_response(f"SafetyStock_{timezone.localtime():%Y%m%d_%H%M}.xlsx", svc.SHEET, DL_HEADERS, rows,
                         [svc.H_CUST, svc.H_QTY])


def safety_history(request):
    data, _ = _data(request.GET)
    codes = [s.customer_code for s, _, _ in data]
    if not request.GET.get("q") and request.GET.get("status", "ACTIVE") == "ALL":
        codes = None   # 전체 조회면 삭제된 Code 이력도 포함
    qs = SafetyHistory.objects.select_related("changed_by")
    if codes is not None:
        qs = qs.filter(customer_code__in=codes)
    rows = [(h.customer_code, h.qty, stamp(h.changed_at), h.change_type, h.changed_by.username) for h in qs]
    return xlsx_response(f"SafetyStock_History_{timezone.localtime():%Y%m%d_%H%M}.xlsx", "History",
                         ["Customer Code", "Safety Q'ty", "Update", "Change Type", "Changed By"], rows)


FLOW = UploadFlow(module=svc.MODULE, ns="safety", title="Safety Stock", file_prefix="SafetyStock",
                  validate=svc.validate, apply=svc.apply, count_labels=svc.COUNT_LABELS)

app_name = "safety"
urlpatterns = [
    path("", safety_list, name="list"),
    path("download.xlsx", safety_download, name="download"),
    path("history.xlsx", safety_history, name="history"),
    *FLOW.urls(),
]
