"""Material Master 정의 (설계/01 B절, 설계/03). 처리 흐름은 core.masterdata 공통."""
from accounts.models import User
from core.excel import to_int, to_text
from core.masterdata import Field, MasterSpec

from .models import Material, MaterialHistory, UnitCode

H_CODE, H_UNIT, H_PUR, H_LT = "Material Code", "Unit", "Purchaser ID", "L/T(Weeks)"


def _context():
    return {"units": set(UnitCode.objects.values_list("code", flat=True)),
            "users": {u.username: u for u in User.objects.all()}}


def parse_unit(raw, ctx):
    """필수, 허용값만, 대문자 변환 (Ⅵ-1-4 ④, H-1)."""
    unit = to_text(raw)
    unit = unit.upper() if unit else None
    if not unit:
        raise ValueError("Unit is required.")
    if unit not in ctx["units"]:
        raise ValueError(f"'{unit}' is not an allowed Unit ({', '.join(sorted(ctx['units']))}).")
    return unit


def parse_purchaser(raw, ctx):
    """선택. 등록된 사용자 ID만 (대소문자 무시, Ⅵ-1-4 ⑤)."""
    pid = to_text(raw)
    pid = pid.lower() if pid else None
    if pid and pid not in ctx["users"]:
        raise ValueError(f"'{pid}' is not a registered user ID.")
    return pid


def parse_lead_time(raw, ctx):
    """필수, 1 이상의 정수 (Ⅵ-1-4 ⑧)."""
    try:
        lt = to_int(raw)
    except ValueError:
        lt = None
    if lt is None or lt < 1:
        raise ValueError("L/T(Weeks) must be a whole number of 1 or more.")
    return lt


def parse_zero_or_more(raw, ctx):
    """v1.1 자재 안전재고·MOQ·Rounding Value: 선택, 빈칸 = 0, 0 이상의 정수."""
    try:
        v = to_int(raw)
    except ValueError:
        v = -1
    if v is None:
        return 0
    if v < 0:
        raise ValueError("Must be a whole number of 0 or more.")
    return v


def _set_unit(obj, v, ctx):
    obj.unit_id = v


def _set_purchaser(obj, v, ctx):
    obj.purchaser = ctx["users"].get(v) if v else None


SPEC = MasterSpec(
    module="M1", sheet="MD_Material", code_header=H_CODE, code_field="material_code",
    model=Material, history=MaterialHistory,
    fields=[
        Field("description", "Desc.", "Desc.", "desc"),
        Field("spec", "Spec.", "Spec.", "spec"),
        Field("unit", H_UNIT, "Unit", "unit", parse_unit, lambda o: o.unit_id, _set_unit),
        Field("purchaser", H_PUR, "Purchaser", "purchaser", parse_purchaser,
              lambda o: o.purchaser.username if o.purchaser else None, _set_purchaser),
        Field("vendor", "Vendor", "Vendor", "vendor"),
        Field("country", "Country", "Country", "country"),
        Field("lead_time_weeks", H_LT, "L/T(Weeks)", "lt", parse_lead_time),
        Field("safety_stock", "Mat. Safety Stock", "Mat. Safety Stock", "ss", parse_zero_or_more),
        Field("moq", "MOQ", "MOQ", "moq", parse_zero_or_more),
        Field("rounding_value", "Rounding Value", "Rounding Value", "rv", parse_zero_or_more),
    ],
    required=[H_UNIT, H_LT],
    banned_codes=frozenset({"ASSY"}),  # Ⅶ-5: BOM의 Assy 열 표식과 혼동 방지
    select_related=("purchaser",),
    context=_context,
)
