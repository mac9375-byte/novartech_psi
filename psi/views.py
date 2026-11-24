"""Module 9 Material Requirement, Module 10 Material PSI (+ Recalculate, Weekly Reset)."""
from collections import defaultdict
from decimal import Decimal

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.permissions import has_perm, require
from core import lookup, weeks
from core.excel import xlsx_response
from core.fmt import frac, num
from core.models import OperationLog, SystemStatus
from core.context import module_context
from core.tablepage import cell, render_table

from . import engine
from .models import MrRow, PsiRow

PLAN_FILTER = [("ALL", "All"), ("RTF", "RTF"), ("PROD", "Prod.")]
PLAN_LABEL = {"RTF": "RTF", "PROD": "Prod."}


def _ctx(request, fields):
    cur = weeks.current_week()
    week = weeks.selected(request.GET, cur)
    plan = request.GET.get("plan", "ALL")
    plan = plan if plan in dict(PLAN_FILTER) else "ALL"
    keys = [f[0] for f in fields]
    field = request.GET.get("field", keys[0])
    field = field if field in keys else keys[0]
    q = (request.GET.get("q") or "").strip()
    controls = {"weeks": weeks.choices(cur), "week": week, "plans": PLAN_FILTER, "plan": plan,
                "fields": fields, "field": field, "q": q}
    return cur, week, plan, field, q, controls


def _plans(plan):
    return ["RTF", "PROD"] if plan == "ALL" else [plan]


def _banners(week):
    """Final Calculation 결과: Warning 요약, BOM 미등록 n건, 자동 생성 n건, 재계산 필요 (Ⅳ-7-2, Ⅲ-4-3)."""
    out = []
    st = SystemStatus.get()
    if st.need_recalculation:
        out.append(("error", "● Need Recalculation — source data changed after the last calculation. "
                             "(재계산 전 원본 기준 차이 있음)"))
    log = OperationLog.objects.filter(kind=OperationLog.Kind.RECALC, week=week, success=True).first()
    if log:
        d = log.details
        if d.get("no_bom"):
            out.append(("warn", f"BOM 미등록 Assy {d['no_bom']}건 – 소요량 0 간주 (Warning)"))
        if d.get("auto_generated"):
            out.append(("info", f"RTF/Prod. 자동 생성 {d['auto_generated']}건"))
    return out, log


def _vals(xs):
    return [Decimal(x) for x in xs]


# ---------------- Module 9 Material Requirement ----------------
MR_FIELDS = [("mat", "Mat. Code"), ("cust", "Cust. Code")]
MR_COLS_FIXED = [("No", "sys"), ("Mat. Code", "sys"), ("Cust. Code", "sys"), ("Desc. / Type", "sys"),
                 ("Spec. / Model", "sys"), ("Plan", "sys"), ("Unit", "sys"), ("Q'ty", "sys")]


def _mr_blocks(week, plan, field, q):
    """Material × Plan 블록: Total 행 → Assy 행(Cust. Code 순). Cust. Code 검색은 그 Assy가 속한 블록 전체."""
    rows = list(MrRow.objects.filter(week=week, plan__in=_plans(plan)))
    blocks = defaultdict(lambda: {"total": None, "assy": []})
    for r in rows:
        b = blocks[r.material_code, r.plan]
        if r.customer_code:
            b["assy"].append(r)
        else:
            b["total"] = r
    out = []
    for (mat, pl), b in sorted(blocks.items(), key=lambda kv: (kv[0][0], kv[0][1] != "RTF")):
        b["assy"].sort(key=lambda r: r.customer_code)
        if q:
            ql = q.lower()
            hit = ql in mat.lower() if field == "mat" else any(ql in r.customer_code.lower() for r in b["assy"])
            if not hit:
                continue
        out.append((mat, pl, b["total"], b["assy"]))
    return out


def mr_list(request):
    cur, week, plan, field, q, controls = _ctx(request, MR_FIELDS)
    blocks = _mr_blocks(week, plan, field, q)
    mats = lookup.materials({m for m, *_ in blocks})
    assies = lookup.assies({r.customer_code for *_, a in blocks for r in a})
    hz = weeks.horizon(week)
    rows, n = [], 0
    for mat, pl, total, arows in blocks:
        m = mats.get(mat)
        n += 1
        st = lookup.status(m)
        rows.append({"cls": "agg blockstart", "cells": [cell(n), cell(mat), cell("Total"), cell(m and m.description),
                     cell(m and m.spec), cell(PLAN_LABEL[pl]), cell(m and m.unit_id), cell("-")]
                     + [cell(num(v, 2), "num") for v in _vals(total.values)] + [cell(st, lookup.status_cls(st))]})
        for r in arows:
            n += 1
            a = assies.get(r.customer_code)
            st = lookup.status(a)
            rows.append({"cells": [cell(n), cell(mat), cell(r.customer_code), cell(a and a.assy_type),
                                   cell(a and a.model_name), cell(PLAN_LABEL[pl]), cell(m and m.unit_id),
                                   cell(frac(r.qty), "num")]
                         + [cell(num(v, 2), "num") for v in _vals(r.values)] + [cell(st, lookup.status_cls(st))]})
    banners, _ = _banners(week)
    labels = [weeks.label(w, week) for w in hz]
    return render_table(request, "M9", "Material Requirement",
                        MR_COLS_FIXED + [(l, "sys") for l in labels] + [("Status", "sys")], rows,
                        controls=controls,
                        buttons=[{"label": "Download", "href": reverse("psi:mr_download") + "?" + request.GET.urlencode()}],
                        banners=banners + [("info", "Requirement = Σ(Assy weekly plan × BOM Q'ty). RTF week 14 "
                                                    "includes Safety Stock. Updated only by Recalculate (Module 10).")])


def mr_download(request):
    cur, week, plan, field, q, _ = _ctx(request, MR_FIELDS)
    blocks = _mr_blocks(week, plan, field, q)
    mats = lookup.materials({m for m, *_ in blocks})
    assies = lookup.assies({r.customer_code for *_, a in blocks for r in a})
    data = []
    for mat, pl, total, arows in blocks:
        m = mats.get(mat)
        data.append([mat, "Total", m and m.description, m and m.spec, PLAN_LABEL[pl], m and m.unit_id, None,
                     *_vals(total.values), lookup.status(m)])
        for r in arows:
            a = assies.get(r.customer_code)
            data.append([mat, r.customer_code, a and a.assy_type, a and a.model_name, PLAN_LABEL[pl],
                         m and m.unit_id, frac(r.qty).replace(",", ""), *_vals(r.values), lookup.status(a)])
    data = [[i, *row] for i, row in enumerate(data, start=1)]
    return xlsx_response(f"MaterialRequirement_{week}_{timezone.localtime():%Y%m%d_%H%M}.xlsx", "MR",
                         ["No", "Mat. Code", "Cust. Code", "Desc. / Type", "Spec. / Model", "Plan", "Unit", "Q'ty",
                          *weeks.horizon(week), "Status"], data)


# ---------------- Module 10 Material PSI ----------------
PSI_FIELDS = [("mat", "Mat. Code"), ("desc", "Desc.")]
PSI_ITEMS = ["Requirement", "Scheduled Receipt", "Inventory Balance", "PO Balance"]


def _psi(week, plan, field, q):
    rows = sorted(PsiRow.objects.filter(week=week, plan__in=_plans(plan)),
                  key=lambda r: (r.material_code, r.plan != "RTF"))
    mats = lookup.materials({r.material_code for r in rows})
    if q:
        ql = q.lower()
        rows = [r for r in rows if ql in (r.material_code if field == "mat"
                                          else (getattr(mats.get(r.material_code), "description", "") or "")).lower()]
    return rows, mats


def _po_titles(week):
    """Open PO 셀 설명: PO No · PO Date · Open 수량 (Ⅶ-11)."""
    from weekly.models import OpenPoRow
    out = defaultdict(list)
    for r in OpenPoRow.objects.filter(week=week):
        if r.open_qty > 0:
            out[r.material_code].append(f"{r.po_no} ({r.po_date}) {num(r.open_qty)}")
    return {k: " / ".join(v) for k, v in out.items()}


def psi_list(request):
    cur, week, plan, field, q, controls = _ctx(request, PSI_FIELDS)
    data, mats = _psi(week, plan, field, q)
    po_titles = _po_titles(week)
    rows, n = [], 0
    for r in data:
        m = mats.get(r.material_code)
        st = lookup.status(m)
        man, calc = _vals(r.sr_manual), _vals(r.sr_calc)
        series = [
            [cell(num(v, 2), "num") for v in _vals(r.req)],
            [cell(num(a + b, 2) if a + b else "", "num calc" if b else "num",
                  f"Manual {num(a, 2)} / Calculated {num(b, 2)}" if b else "") for a, b in zip(man, calc)],
            [cell(num(v, 2), "num negcell" if v < 0 else "num") for v in _vals(r.inv_balance)],
            [cell(num(v, 2), "num negcell" if v < 0 else "num") for v in _vals(r.po_balance)],
        ]
        for i, (item, values) in enumerate(zip(PSI_ITEMS, series)):
            n += 1
            rows.append({"cls": ("agg blockstart" if i == 0 else ""),
                         "cells": [cell(n), cell(r.material_code), cell(m and m.description), cell(m and m.spec),
                                   cell(m and m.unit_id), cell(num(r.opening, 2), "num"),
                                   cell(num(r.open_po, 2), "num", po_titles.get(r.material_code, "")),
                                   cell(PLAN_LABEL[r.plan]), cell(item)] + values
                                  + [cell(st if i == 0 else "", lookup.status_cls(st))]})
    banners, log = _banners(week)
    if log and log.details.get("warnings"):
        banners.append(("warn", f"Warnings in last calculation: {len(log.details['warnings'])} "
                                "(details: 'Operation log' download)."))
    is_cur = week == cur
    can_calc = has_perm(request.user, "recalculate") and is_cur
    can_reset = has_perm(request.user, "weekly_reset") and is_cur
    qs = request.GET.urlencode()
    labels = [weeks.label(w, week) for w in weeks.horizon(week)]
    cols = ([("No", "sys"), ("Mat. Code", "sys"), ("Desc.", "sys"), ("Spec.", "sys"), ("Unit", "sys"),
             ("Opening Inventory", "sys"), ("Open PO", "sys"), ("Plan", "sys"), ("PSI", "sys")]
            + [(l, "sys") for l in labels] + [("Status", "sys")])
    return render(request, "psi/psi.html", module_context(
        "M10", page_title="Material PSI", columns=cols, rows=rows, controls=controls, banners=banners,
        query_string=qs, upload=None, reset_done=request.GET.get("reset") == "done",
        buttons=[{"kind": "dialog", "label": "Weekly Reset", "dialog": "reset-dialog", "disabled": not can_reset},
                 {"kind": "post", "label": "Recalculate", "form": "recalc-form", "primary": True,
                  "disabled": not can_calc},
                 {"label": "Download", "href": reverse("psi:psi_download") + "?" + qs},
                 {"label": "Operation log", "href": reverse("psi:log_download") + "?week=" + week}],
    ))


def psi_download(request):
    cur, week, plan, field, q, _ = _ctx(request, PSI_FIELDS)
    data, mats = _psi(week, plan, field, q)
    out = []
    for r in data:
        m = mats.get(r.material_code)
        sr = [a + b for a, b in zip(_vals(r.sr_manual), _vals(r.sr_calc))]
        for item, values in zip(PSI_ITEMS, (_vals(r.req), sr, _vals(r.inv_balance), _vals(r.po_balance))):
            out.append([r.material_code, m and m.description, m and m.spec, m and m.unit_id, r.opening, r.open_po,
                        PLAN_LABEL[r.plan], item, *values, lookup.status(m)])
    out = [[i, *row] for i, row in enumerate(out, start=1)]
    return xlsx_response(f"MaterialPSI_{week}_{timezone.localtime():%Y%m%d_%H%M}.xlsx", "PSI",
                         ["No", "Mat. Code", "Desc.", "Spec.", "Unit", "Opening Inventory", "Open PO", "Plan", "PSI",
                          *weeks.horizon(week), "Status"], out)


def log_download(request):
    """Recalculate / Weekly Reset 기록 + 마지막 계산의 Error·Warning 목록."""
    week = weeks.selected(request.GET)
    rows = []
    for log in OperationLog.objects.filter(week=week).select_related("user"):
        lines = log.details.get("errors", []) + log.details.get("warnings", []) or [""]
        for line in lines:
            rows.append((timezone.localtime(log.at).strftime("%Y-%m-%d %H:%M"), log.get_kind_display(),
                         log.user.username, "Success" if log.success else "Failed", log.error_count,
                         log.warning_count, line))
    return xlsx_response(f"OperationLog_{week}.xlsx", "Log",
                         ["Time", "Operation", "User", "Result", "Errors", "Warnings", "Detail"], rows)


@require_POST
@require("recalculate")
def recalc_view(request):
    week = weeks.current_week()   # 재계산은 Current Week만 (Ⅳ-7-1)
    try:
        log = engine.recalculate(week, request.user)
    except engine.RecalcBusy as e:
        messages.error(request, str(e))
        return redirect("psi:psi")
    if log.success:
        messages.success(request, f"{week} 재계산이 완료되었습니다. 영향 Module: Material Requirement, Material PSI "
                                  f"(Recalculation completed at {timezone.localtime(log.at):%Y-%m-%d %H:%M}, "
                                  f"warnings {log.warning_count}).")
    else:
        messages.error(request, f"{week} Recalculation failed — {log.error_count} error(s). Previous results are kept. "
                                + " | ".join(log.details["errors"][:5]))
    return redirect("psi:psi")


@require_POST
@require("weekly_reset")
def reset_view(request):
    week = weeks.current_week()
    engine.weekly_reset(week, request.user)
    return redirect(reverse("psi:psi") + "?reset=done")


app_name = "psi"
urlpatterns = [
    path("material-requirement/", mr_list, name="mr"),
    path("material-requirement/download.xlsx", mr_download, name="mr_download"),
    path("material-psi/", psi_list, name="psi"),
    path("material-psi/download.xlsx", psi_download, name="psi_download"),
    path("material-psi/log.xlsx", log_download, name="log_download"),
    path("material-psi/recalculate/", recalc_view, name="recalculate"),
    path("material-psi/weekly-reset/", reset_view, name="reset"),
]
