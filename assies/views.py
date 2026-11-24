from core.masterviews import MasterScreen, stamp

from .services import SPEC

HEADERS = ["No", "Customer Code", "Assy Code", "Type", "Model", "Item", "Customer", "Country", "Update", "Status"]


def _row(n, a):
    return (n, a.customer_code, a.assy_code, a.assy_type, a.model_name, a.item, a.customer, a.country,
            stamp(a.updated_at), a.get_status_display())


def _history_row(n, h):
    return (n, h.customer_code, h.assy_code, h.assy_type, h.model_name, h.item, h.customer, h.country,
            stamp(h.changed_at), h.status.title(), h.change_type, h.changed_by.username)


SCREEN = MasterScreen(
    spec=SPEC, ns="assies", title="Assy Master", file_prefix="AssyMaster", template="assies/list.html",
    search_fields=[
        ("cust", "Cust. Code", ["customer_code"]),
        ("assy", "Assy Code", ["assy_code"]),
        ("type", "Type", ["assy_type"]),
        ("model", "Model", ["model_name"]),
        ("item", "Item", ["item"]),
        ("customer", "Customer", ["customer"]),
        ("country", "Country", ["country"]),
    ],
    download_headers=HEADERS, download_row=_row, history_row=_history_row,
)
