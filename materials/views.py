from accounts.models import IdStatus, User
from core.masterviews import MasterScreen, stamp

from .models import UnitCode
from .services import SPEC

HEADERS = ["No", "Material Code", "Desc.", "Spec.", "Unit", "Purchaser ID", "Purchaser",
           "Vendor", "Country", "L/T(Weeks)", "Mat. Safety Stock", "MOQ",
           "Rounding Value", "Update", "Status"]


def _row(n, m):
    return (n, m.material_code, m.description, m.spec, m.unit_id,
            m.purchaser.username if m.purchaser else None, m.purchaser.name if m.purchaser else None,
            m.vendor, m.country, m.lead_time_weeks, m.safety_stock, m.moq, m.rounding_value, stamp(m.updated_at),
            m.get_status_display())


def _history_row(n, h):
    return (n, h.material_code, h.description, h.spec, h.unit, h.purchaser_id_text, h.purchaser_name,
            h.vendor, h.country, h.lead_time_weeks, h.safety_stock, h.moq, h.rounding_value, stamp(h.changed_at), h.status.title(),
            h.change_type, h.changed_by.username)


SCREEN = MasterScreen(
    spec=SPEC, ns="materials", title="Material Master", file_prefix="MaterialMaster",
    template="materials/list.html",
    search_fields=[
        ("code", "Mat. Code", ["material_code"]),
        ("desc", "Desc.", ["description"]),
        ("purchaser", "Purchaser", ["purchaser__name", "purchaser__username"]),
        ("vendor", "Vendor", ["vendor"]),
        ("country", "Country", ["country"]),
    ],
    download_headers=HEADERS, download_row=_row, history_row=_history_row,
    extra_context=lambda request: {"units": UnitCode.objects.all(),
                                   "users": User.objects.order_by("name", "username"),
                                   "approved": IdStatus.APPROVED},
)
