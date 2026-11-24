"""Assy Master 정의 (Ⅵ-2, 설계/04). 처리 흐름은 core.masterdata 공통."""
from core.masterdata import Field, MasterSpec, parse_code_attr

from .models import Assy, AssyHistory

SPEC = MasterSpec(
    module="M2", sheet="MD_Assy", code_header="Customer Code", code_field="customer_code",
    model=Assy, history=AssyHistory,
    fields=[
        Field("assy_code", "Assy Code", "Assy Code", "assy", parse_code_attr),
        Field("assy_type", "Type", "Type", "type"),       # Header 'Type' (H-7)
        Field("model_name", "Model", "Model", "model"),
        Field("item", "Item", "Item", "item"),
        Field("customer", "Customer", "Customer", "customer"),
        Field("country", "Country", "Country", "country"),
    ],
    required=[],  # 필수는 Customer Code뿐 (Ⅵ-2-5)
)
