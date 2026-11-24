"""Module 5~8 화면. 작업 주차 Dropdown(Current Week ~ 지난 16주), 과거 주차는 조회·Download만 (Ⅳ-6-2)."""

from django.urls import include, path, reverse
from django.utils import timezone

from accounts.permissions import has_perm
from core import lookup, weeks
from core.excel import xlsx_response
from core.fmt import num
from core.tablepage import cell, render_table
from core.uploadflow import UploadFlow

from . import services as svc
from .models import InventoryRow, OpenPoRow, PlanRow

PLAN_FILTER = [("ALL", "All"), ("RTF", "RTF"), ("PROD", "Prod.")]


def _ctx(request, fields):
    cur = weeks.current_week()
    week = weeks.selected(request.GET, cur)
    keys = [f[0] for f in fields]
    field = request.GET.get("field", keys[0]) if fields else ""
    field = field if field in keys else (keys[0] if keys else "")
    q = (request.GET.get("q") or "").strip()
    controls = {"weeks": weeks.choices(cur), "week": week, "fields": fields, "field": field, "q": q}
    return cur, week, field, q, controls


def _buttons(request, ns, week, cur, note):
    """Upload은 Admin + 작업 주차가 Current Week일 때만 (과거 주차 Upload 불가)."""
    can_up = has_perm(request.user, "upload") and week == cur
    qs = request.GET.urlencode()
    buttons = [{"kind": "upload", "label": "Upload", "disabled": not can_up},
               {"label": "Download", "href": reverse(f"{ns}:download") + "?" + qs}]
    if has_perm(request.user, "upload"):
        buttons.append({"label": "Template", "href": reverse(f"{ns}:template")})
    upload = {"action": reverse(f"{ns}:upload"), "note": note + f" · Working week: {cur} (W0). "
              "Existing data of this week is replaced (전체교체)."} if can_up else None
    banners = [] if week == cur else [("info", f"Past week {week}: view and download only. (과거 주차: 조회·Download만 가능)")]
    return buttons, upload, banners


def _match(q, *values):
    return not q or any(q.lower() in (v or "").lower() for v in values)


def _week_cols(week, last_label=None):
    hz = weeks.horizon(week)
    labels = [weeks.label(w, week) for w in hz]
    if last_label:
        labels[-1] = last_label
    return hz, labels


def _stamp():
    return f"{timezone.localtime():%Y%m%d_%H%M}"


# ---------------- Module 5 Inventory ----------------
INV_FIELDS = [("code", "Code")]


def _inventory(week, q):
    rows = [r for r in InventoryRow.objects.filter(week=week) if _match(q, r.code)]
    rows.sort(key=lambda r: (r.category != "ASSY", r.code))   # Assy → Material, Code 오름차순
    mats = lookup.materials([r.code for r in rows if r.category == "MATERIAL"])
    assies = lookup.assies([r.code for r in rows if r.category == "ASSY"])
    out = []
    for r in rows:
        o = (assies if r.category == "ASSY" else mats).get(r.code)
        ref = (o.assy_type if r.category == "ASSY" else o.description) if o else None
        out.append((r, lookup.status(o), ref))
    return out


def inventory_list(request):
    cur, week, _, q, controls = _ctx(request, INV_FIELDS)
    rows = [{"cells": [cell(n), cell(r.get_category_display()), cell(r.code), cell(r.unit), cell(num(r.qty), "num"),
                       cell(st, lookup.status_cls(st)), cell(ref)]}
            for n, (r, st, ref) in enumerate(_inventory(week, q), start=1)]
    buttons, upload, banners = _buttons(request, "inventory", week, cur, "Sheet: INVENTORY · Category / Code / Unit / Stock Q'ty")
    return render_table(request, "M5", "Inventory",
                        [("No", "sys"), ("Category", "up"), ("Code", "up"), ("Unit", "up"), ("Stock Q'ty", "up"),
                         ("Status", "sys"), ("Type / Desc.", "sys")],
                        rows, controls=controls, buttons=buttons, upload=upload,
                        banners=banners + [("info", "Stock at Monday morning of the working week (TOTAL). "
                                                    "Material stock: RTF & Prod. / Assy stock: RTF only.")])


def inventory_download(request):
    _, week, _, q, _ = _ctx(request, INV_FIELDS)
    data = [(n, r.get_category_display(), r.code, r.unit, r.qty, st, ref)
            for n, (r, st, ref) in enumerate(_inventory(week, q), start=1)]
    return xlsx_response(f"Inventory_{week}_{_stamp()}.xlsx", svc.INV_SHEET,
                         ["No", *svc.INV_H, "Status", "Type / Desc."], data, svc.INV_H)


# ---------------- Module 6 RTF / Production Plan ----------------
PLAN_FIELDS = [("cust", "Cust. Code"), ("assy", "Assy Code"), ("type", "Type")]


def _plans(request, week, field, q):
    from bom.services import registered
    from safety.services import safety_map
    plan = request.GET.get("plan", "ALL")
    plan = plan if plan in dict(PLAN_FILTER) else "ALL"
    qs = PlanRow.objects.filter(week=week)
    if plan != "ALL":
        qs = qs.filter(plan=plan)
    rows = sorted(qs, key=lambda r: (r.customer_code, r.plan != "RTF"))
    assies = lookup.assies({r.customer_code for r in rows})
    boms, safety = registered({r.customer_code for r in rows}), safety_map()
    out = []
    for r in rows:
        a = assies.get(r.customer_code)
        if not _match(q, {"cust": r.customer_code, "assy": a and a.assy_code, "type": a and a.assy_type}[field]):
            continue
        shown = list(r.qty)
        if r.plan == "RTF":
            shown[-1] += safety.get(r.customer_code, 0)   # 14주차 = 업로드 수량 + Safety Stock (Ⅲ-4-1)
        out.append((r, a, shown, r.customer_code not in boms))
    return plan, out


def plan_list(request):
    cur, week, field, q, controls = _ctx(request, PLAN_FIELDS)
    plan, data = _plans(request, week, field, q)
    controls.update(plans=PLAN_FILTER, plan=plan)
    _, labels = _week_cols(week, "Safety(W+13)")
    rows = []
    for n, (r, a, shown, no_bom) in enumerate(data, start=1):
        st = lookup.status(a)
        rows.append({"cells": [cell(n), cell(r.customer_code), cell(a and a.assy_code), cell(a and a.assy_type),
                               cell(a and a.model_name), cell(a and a.item),
                               cell(r.get_plan_display(), title="Auto-generated (0)" if r.auto else "")]
                     + [cell(num(v), "num") for v in shown]
                     + [cell(st, lookup.status_cls(st)), cell("NO" if no_bom else "", "st-nodb")]})
    buttons, upload, banners = _buttons(request, "plans", week, cur,
                                        "Sheets: RTF and/or PROD_PLAN · Customer Code / Plan / 14 weeks")
    no_bom = len({r.customer_code for r, _, s, nb in data if nb and sum(r.qty) > 0})
    if no_bom:
        banners.append(("warn", f"BOM 미등록 Assy {no_bom}건 – requirement counted as 0 (Warning). "
                                "Admin: register the BOM in Module 3."))
    cols = ([("No", "sys"), ("Cust. Code", "up"), ("Assy Code", "sys"), ("Type", "sys"), ("Model", "sys"),
             ("Item", "sys"), ("Plan", "up")] + [(l, "up") for l in labels] + [("Status", "sys"), ("No BOM", "sys")])
    return render_table(request, "M6", "RTF/Production", cols, rows, controls=controls, buttons=buttons,
                        upload=upload, banners=banners)


def plan_download(request):
    """업로드 원본값 (Safety 합산 제외, 자동 생성 행은 0, M6-3). RTF / PROD_PLAN 시트로 나눔."""
    _, week, field, q, _ = _ctx(request, PLAN_FIELDS)
    _, data = _plans(request, week, field, q)
    hz = weeks.horizon(week)
    sheets = []
    for plan, sheet, label in (("RTF", "RTF", "RTF"), ("PROD", "PROD_PLAN", "Prod.")):
        rows = [(r.customer_code, label, *r.qty, a and a.assy_code, a and a.assy_type, lookup.status(a),
                 "NO" if nb else "") for r, a, _, nb in data if r.plan == plan]
        sheets.append((sheet, ["Customer Code", "Plan", *hz, "Assy Code", "Type", "Status", "No BOM"], rows))
    return xlsx_multi(f"RTF_Production_{week}_{_stamp()}.xlsx", sheets, ["Customer Code", "Plan", *hz])


def xlsx_multi(filename, sheets, upload_headers):
    import io
    from django.http import HttpResponse
    from openpyxl import Workbook
    from core.excel import _BLUE, _GRAY, _HEADER_FONT
    wb = Workbook()
    wb.remove(wb.active)
    for title, headers, rows in sheets:
        ws = wb.create_sheet(title)
        ws.append(headers)
        for c in ws[1]:
            c.font, c.fill = _HEADER_FONT, _BLUE if c.value in upload_headers else _GRAY
        for r in rows:
            ws.append(list(r))
        ws.freeze_panes = "A2"
    buf = io.BytesIO()
    wb.save(buf)
    resp = HttpResponse(buf.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    resp["Content-Disposition"] = f'attachment; filename="{filename}"'
    return resp


# ---------------- Module 7 Open PO ----------------
PO_FIELDS = [("date", "PO Date"), ("pono", "PO No"), ("mat", "Mat. Code"), ("vendor", "Vendor")]
PO_COLS = [("No", "sys"), ("PO Date", "up"), ("PO No", "up"), ("Mat. Code", "up"), ("Unit", "up"), ("PO Q'ty", "up"),
           ("Curr.", "up"), ("Unit Price", "up"), ("Amount", "sys"), ("Cancel", "up"), ("Final PO (+/-)", "sys"),
           ("G/R", "up"), ("In Transit", "up"), ("Remain Q'ty (+/-)", "sys"), ("Remain Amount", "sys"),
           ("Vendor", "up"), ("Status", "sys")]


def _open_po(week, field, q):
    rows = [r for r in OpenPoRow.objects.filter(week=week)
            if _match(q, {"date": r.po_date.isoformat(), "pono": r.po_no, "mat": r.material_code,
                          "vendor": r.vendor}[field])]
    mats = lookup.materials({r.material_code for r in rows})
    return [(r, lookup.status(mats.get(r.material_code))) for r in rows]


def openpo_list(request):
    cur, week, field, q, controls = _ctx(request, PO_FIELDS)
    rows = []
    for n, (r, st) in enumerate(_open_po(week, field, q), start=1):
        rows.append({"cells": [cell(n), cell(r.po_date.isoformat()), cell(r.po_no), cell(r.material_code), cell(r.unit),
                               cell(num(r.po_qty), "num"), cell(r.currency), cell(num(r.unit_price), "num"),
                               cell(num(r.amount, 2), "num"), cell(num(r.cancel), "num"), cell(num(r.final_po), "num"),
                               cell(num(r.gr), "num"), cell(num(r.in_transit), "num"), cell(num(r.remain), "num"),
                               cell(num(r.remain_amount, 2), "num"), cell(r.vendor), cell(st, lookup.status_cls(st))]})
    buttons, upload, banners = _buttons(request, "openpo", week, cur,
                                        "Sheet: OPEN_PO · upload ALL POs including Remain 0")
    return render_table(request, "M7", "Open PO", PO_COLS, rows, controls=controls, buttons=buttons, upload=upload,
                        banners=banners + [("info", "Final PO = PO Q'ty − Cancel · Remain = Final PO − G/R − In Transit · "
                                                    "Open PO = In Transit + Remain (rows > 0 are used)")])


def openpo_download(request):
    _, week, field, q, _ = _ctx(request, PO_FIELDS)
    data = [(n, r.po_date, r.po_no, r.material_code, r.unit, r.po_qty, r.currency, r.unit_price, r.amount, r.cancel,
             r.final_po, r.gr, r.in_transit, r.remain, r.remain_amount, r.vendor, st)
            for n, (r, st) in enumerate(_open_po(week, field, q), start=1)]
    headers = ["No", "PO Date", "PO No", "Material Code", "Unit", "PO Q'ty", "Currency", "Unit Price", "Amount",
               "Cancel", "Final PO", "G/R", "In Transit", "Remain Q'ty", "Remain Amount", "Vendor", "Status"]
    return xlsx_response(f"OpenPO_{week}_{_stamp()}.xlsx", svc.PO_SHEET, headers, data, svc.PO_REQ + svc.PO_OPT)


# ---------------- Module 8 Scheduled Receipt ----------------
SR_FIELDS = [("mat", "Mat. Code"), ("vendor", "Vendor"), ("lt", "L/T")]


def _sched(week, field, q):
    out = []
    for item in svc.scheduled_receipts(week).values():
        m = item["material"]
        lt = str(m.lead_time_weeks) if m else ""
        if not _match(q, {"mat": item["mat"], "vendor": item["vendor"], "lt": lt}[field]):
            continue
        out.append(item)
    return out


def sched_list(request):
    cur, week, field, q, controls = _ctx(request, SR_FIELDS)
    _, labels = _week_cols(week)
    rows, negatives = [], []
    for n, it in enumerate(_sched(week, field, q), start=1):
        m = it["material"]
        st = lookup.status(m)
        cells = [cell(n), cell(it["mat"]), cell(it["vendor"]), cell(it["unit"])]
        for man, calc in zip(it["manual"], it["calc"]):
            total = man + calc
            cells.append(cell(num(total) if total else "", "num calc" if calc else "num",
                              f"Manual {num(man)} / Calculated {num(calc)}" if calc else ""))
        cells += [cell(num(it["in_transit"]), "num"), cell(num(it["remain"]), "num"),
                  cell(m.lead_time_weeks if m else ""), cell(st, lookup.status_cls(st))]
        rows.append({"cells": cells})
        if it["diff"] < 0:
            negatives.append(f"{it['mat']} / {it['vendor']}")
    buttons, upload, banners = _buttons(request, "sched", week, cur,
                                        "Sheet: SCHED_RECEIPT · Material Code / Vendor / Unit / 14 weeks · "
                                        "Upload Open PO of this week first")
    if negatives:
        banners.append(("error", "Scheduled Receipt is greater than Open PO (차이분 음수): " + ", ".join(negatives)))
    banners.append(("info", "Black = Manual (uploaded) · Blue = Calculated: (Open PO − Manual total) placed at "
                            "working week + L/T (W+13 if beyond)."))
    cols = ([("No", "sys"), ("Mat. Code", "up"), ("Vendor", "up"), ("Unit", "up")] + [(l, "up") for l in labels]
            + [("Open PO: In Transit", "sys"), ("Open PO: Remain Q'ty", "sys"), ("L/T (W)", "sys"), ("Status", "sys")])
    return render_table(request, "M8", "Scheduled Receipt", cols, rows, controls=controls, buttons=buttons,
                        upload=upload, banners=banners)


def sched_download(request):
    """Manual 원본값만 (계산 입고예정 제외, Ⅵ-8-9)."""
    _, week, field, q, _ = _ctx(request, SR_FIELDS)
    hz = weeks.horizon(week)
    data = [(n, it["mat"], it["vendor"], it["unit"], *it["manual"], it["in_transit"], it["remain"],
             it["material"].lead_time_weeks if it["material"] else None, lookup.status(it["material"]))
            for n, it in enumerate(_sched(week, field, q), start=1)]
    headers = ["No", "Material Code", "Vendor", "Unit", *hz, "Open PO In Transit", "Open PO Remain Q'ty", "L/T", "Status"]
    return xlsx_response(f"ScheduledReceipt_{week}_{_stamp()}.xlsx", svc.SR_SHEET, headers, data,
                         ["Material Code", "Vendor", "Unit", *hz])


# ---------------- Template (빈 양식, 작업 주차 Header 포함) ----------------
def _template(sheets_fn, name):
    def view(request):
        hz = weeks.horizon(weeks.current_week())
        return xlsx_multi(f"{name}_Template_{hz[0]}.xlsx", [(s, h, []) for s, h in sheets_fn(hz)],
                          [h for _, hs in sheets_fn(hz) for h in hs])
    return view


def _module(ns, module, title, prefix, list_view, download_view, validate, apply, labels, template, depends=()):
    from accounts.permissions import require
    flow = UploadFlow(module=module, ns=ns, title=title, file_prefix=prefix, validate=validate, apply=apply,
                      count_labels=labels, weekly=True, depends=depends)
    patterns = [path("", list_view, name="list"), path("download.xlsx", download_view, name="download"),
                path("template.xlsx", require("upload")(template), name="template"), *flow.urls()]
    return include((patterns, ns), namespace=ns)


urlpatterns = [
    path("inventory/", _module("inventory", "M5", "Inventory", "Inventory", inventory_list, inventory_download,
                               svc.inventory_validate, svc.inventory_apply, svc.REPLACE_LABELS,
                               _template(lambda hz: [(svc.INV_SHEET, svc.INV_H)], "Inventory"))),
    path("rtf-production/", _module("plans", "M6", "RTF/Production", "RTF_Production", plan_list, plan_download,
                                    svc.plan_validate, svc.plan_apply, svc.PLAN_LABELS,
                                    _template(lambda hz: [("RTF", ["Customer Code", "Plan", *hz]),
                                                          ("PROD_PLAN", ["Customer Code", "Plan", *hz])], "RTF_PROD"))),
    path("open-po/", _module("openpo", "M7", "Open PO", "OpenPO", openpo_list, openpo_download,
                             svc.openpo_validate, svc.openpo_apply, svc.REPLACE_LABELS,
                             _template(lambda hz: [(svc.PO_SHEET, ["PO Date", "PO No", "Material Code", "Unit", "PO Q'ty",
                                                                   "Currency", "Unit Price", "Cancel", "G/R",
                                                                   "In Transit", "Vendor"])], "OPEN_PO"),
                             depends=("M8",))),
    path("scheduled-receipt/", _module("sched", "M8", "Scheduled Receipt", "ScheduledReceipt", sched_list,
                                       sched_download, svc.sched_validate, svc.sched_apply, svc.REPLACE_LABELS,
                                       _template(lambda hz: [(svc.SR_SHEET, ["Material Code", "Vendor", "Unit", *hz])],
                                                 "SCHED_RECEIPT"), depends=("M7",))),
]
