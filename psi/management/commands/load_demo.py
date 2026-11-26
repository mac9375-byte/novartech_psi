"""PoC 점검용 예시 데이터 (Code는 모두 'DEMO-'로 시작).

    .venv\\Scripts\\python manage.py load_demo           # 예시 데이터 적재 + Recalculate
    .venv\\Scripts\\python manage.py load_demo --clear   # 예시 데이터만 삭제

실제 Upload 화면과 같은 처리(검증 → 반영)를 거쳐 적재한다. 값은 UI 도안(PPT) 예시를 참고했다.
"""
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.test import Client

from accounts.models import IdStatus, User, UserClass
from core import weeks
from core.models import SystemStatus, UploadBatch
from core.testutil import xlsx

P = "DEMO-"
MATS = [  # code, desc, spec, unit, vendor, country, L/T, Mat. Safety Stock, MOQ, Rounding Value (v1.1)
    ("SMMZ14001", "Magnet", "d7*0.4, N30SH", "EA", "YX", "China", 8, 15000, 10000, 4000),
    ("SMCZ13001", "Cap", "D7.5*0.6(d7*0.4)", "EA", "LS", "Korea", 4, 2000, 5000, 0),
    ("SMCZ25009", "Holder", "12x10.6t, Brass", "EA", "YX", "China", 6, 0, 0, 0),
    ("CMAD15000", "Epoxy (BOND)", "TB2212_gram", "G", "MASTER CHEMICAL", "Korea", 3, 0, 0, 0),
    ("BOLT3535", "BOLT", "M5*6,8,12, M3*10", "SET", "SOHUCO", "Vina", 2, 0, 0, 0),
]
ASSIES = [  # customer code, assy code, type, model, item
    ("GH00-00000B", "SMAZ13001", "Shield Magnet", "[SM-S911] Galaxy S23", "D7.5*0.6(d7*0.4), N30SH"),
    ("GH00-00012A", "SMAZ14002", "Magnet", "[SM-F741U] Z FLIP6", "B6 MAIN L"),
    ("GH00-00145A", "SMAZ14006", "Epoxy Plate", "[EF-BX900] Tab S8 Ultra", "Assy Epoxy Front"),
    ("GH00-00254A", "SMAZ14011", "Halbah", "[SM-F926U] Galaxy Z Fold3", "Q2 MAIN MAGNET MID"),
]
BOM = {  # customer code: [(material, unit, qty)]
    "GH00-00000B": [("SMMZ14001", "EA", 2), ("SMCZ13001", "EA", 1), ("CMAD15000", "G", "1/50")],
    "GH00-00012A": [("SMMZ14001", "EA", 2), ("SMCZ25009", "EA", 1)],
    "GH00-00145A": [("CMAD15000", "G", "1/20"), ("BOLT3535", "SET", 1)],
    # GH00-00254A: BOM 미등록 예시
}
SAFETY = {"GH00-00000B": 500, "GH00-00012A": 300, "GH00-00145A": 200}
RTF = {
    "GH00-00000B": [200, 300, 150, 400, 100, 150, 200, 135, 200, 400, 120, 400, 300, 0],
    "GH00-00012A": [300, 400, 450, 200, 400, 300, 200, 400, 300, 400, 100, 150, 200, 0],
    "GH00-00145A": [100, 100, 120, 120, 150, 150, 150, 100, 100, 100, 80, 80, 80, 0],
    "GH00-00254A": [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 0],
}
PROD = {
    "GH00-00000B": [100, 300, 250, 300, 100, 100, 250, 135, 300, 300, 150, 350, 200, 300],
    "GH00-00012A": [300, 400, 450, 200, 400, 300, 200, 400, 300, 400, 100, 150, 170, 400],
}
INVENTORY = [("Assy", "GH00-00000B", "", 500), ("Assy", "GH00-00012A", "", 300),
             ("Material", "SMMZ14001", "EA", 5000), ("Material", "SMCZ13001", "EA", 4000),
             ("Material", "SMCZ25009", "EA", 1000), ("Material", "CMAD15000", "G", 120.5),
             ("Material", "BOLT3535", "SET", 600)]
OPEN_PO = [  # date, PO No, material, unit, PO Q'ty, curr, price, cancel, G/R, in transit, vendor
    (date(2026, 6, 6), "PO YX260606-01", "SMMZ14001", "EA", 50000, "USD", 0.7501, 10000, 20000, 5000, "YX"),
    (date(2026, 7, 20), "PO YX260720-02", "SMCZ25009", "EA", 20000, "USD", 1.253, 0, 15000, 2000, "YX"),
    (date(2026, 8, 2), "PO LS260802-02", "SMCZ13001", "EA", 30000, "USD", 0.3245, 10000, 20000, None, "LS"),
    (date(2026, 9, 10), "PO SO260910-01", "BOLT3535", "SET", 3000, "VND", 1500, None, 1000, 500, "SOHUCO"),
]
SCHED = [("SMMZ14001", "YX", "EA", {0: 3000, 2: 2500, 3: 1500, 5: 4000}),
         ("SMCZ25009", "YX", "EA", {0: 2000, 1: 1500}),
         ("BOLT3535", "SOHUCO", "SET", {0: 500, 2: 600})]


class Command(BaseCommand):
    help = "Load (or --clear) PoC demo data. All codes start with 'DEMO-'."

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Delete demo data only")

    def handle(self, *args, **opts):
        if opts["clear"]:
            self.clear()
            return
        from materials.models import Material
        if Material.objects.filter(material_code__startswith=P).exists():
            raise CommandError("Demo data already exists. Run 'load_demo --clear' first.")
        admin = (User.objects.filter(user_class=UserClass.ADMIN, id_status=IdStatus.APPROVED).first()
                 or User.objects.filter(username="poc_admin").first())
        if not admin:
            raise CommandError("No approved Admin user. Approve an Admin first.")
        c = Client(SERVER_NAME="localhost")
        c.force_login(admin)
        hz = weeks.horizon(weeks.current_week())

        def up(prefix, title, sheets, upload_type=""):
            c.post(f"{prefix}upload/", {"upload_type": upload_type, "file": xlsx(sheets)})
            b = UploadBatch.objects.latest("id")
            if b.state == UploadBatch.State.PREVIEW:
                c.post(f"{prefix}upload/{b.pk}/apply/")
                b.refresh_from_db()
            errors = [i["reason"] for i in b.issues if i["level"] == "Error"]
            self.stdout.write(f"{title:<20} {b.state:<8} warnings {b.warning_count}" + (f" errors {errors[:3]}" if errors else ""))
            if b.state != UploadBatch.State.APPLIED:
                raise CommandError(f"{title} upload failed.")

        up("/material-master/", "Material Master", {"MD_Material": [
            ["Material Code", "Desc.", "Spec.", "Unit", "Purchaser ID", "Vendor", "Country", "L/T(Weeks)",
             "Mat. Safety Stock", "MOQ", "Rounding Value"],
            *[[P + c_, d, s, u, admin.username, v, co, lt, ss, moq, rv]
              for c_, d, s, u, v, co, lt, ss, moq, rv in MATS]]}, "CHANGE")
        up("/assy-master/", "Assy Master", {"MD_Assy": [
            ["Customer Code", "Assy Code", "Type", "Model", "Item", "Customer", "Country"],
            *[[P + c_, a, t, m, i, "SEVT", "Vina"] for c_, a, t, m, i in ASSIES]]}, "CHANGE")
        bom_rows = [["Customer Code", "Material Code", "Unit", "Q'ty"]]
        for cust, lines in BOM.items():
            bom_rows.append([P + cust, "Assy"])
            bom_rows += [[P + cust, P + m, u, q] for m, u, q in lines]
        up("/bom/", "BOM", {"BOM": bom_rows}, "CHANGE")
        up("/safety-stock/", "Safety Stock", {"SAFETY": [["Customer Code", "Safety Q'ty"],
                                                         *[[P + k, v] for k, v in SAFETY.items()]]})
        up("/inventory/", "Inventory", {"INVENTORY": [["Category", "Code", "Unit", "Stock Q'ty"],
                                                      *[[cat, P + code, u, q] for cat, code, u, q in INVENTORY]]})
        up("/rtf-production/", "RTF/Production", {
            "RTF": [["Customer Code", "Plan", *hz], *[[P + k, "RTF", *v] for k, v in RTF.items()]],
            "PROD_PLAN": [["Customer Code", "Plan", *hz], *[[P + k, "Prod.", *v] for k, v in PROD.items()]]})
        up("/open-po/", "Open PO", {"OPEN_PO": [
            ["PO Date", "PO No", "Material Code", "Unit", "PO Q'ty", "Currency", "Unit Price", "Cancel", "G/R",
             "In Transit", "Vendor"], *[[d, n, P + m, *rest] for d, n, m, *rest in OPEN_PO]]})
        up("/scheduled-receipt/", "Scheduled Receipt", {"SCHED_RECEIPT": [
            ["Material Code", "Vendor", "Unit", *hz],
            *[[P + m, v, u, *[q.get(i) for i in range(14)]] for m, v, u, q in SCHED]]})

        c.post("/material-psi/recalculate/")
        st = SystemStatus.get()
        self.stdout.write(self.style.SUCCESS(
            f"Demo data loaded for {hz[0]} and recalculated (by {admin.username}). "
            f"Need Recalculation: {st.need_recalculation}"))

    def clear(self):
        from assies.models import Assy, AssyHistory
        from bom.models import BomVersion
        from materials.models import Material, MaterialHistory
        from psi.models import MrRow, PsiRow
        from safety.models import SafetyHistory, SafetyStock
        from weekly.models import InventoryRow, OpenPoRow, PlanRow, SchedRow
        total = 0
        for model, field in [(MrRow, "material_code"), (PsiRow, "material_code"), (InventoryRow, "code"),
                             (PlanRow, "customer_code"), (OpenPoRow, "material_code"), (SchedRow, "material_code"),
                             (SafetyHistory, "customer_code"), (SafetyStock, "customer_code"),
                             (BomVersion, "customer_code"), (MaterialHistory, "material_code"),
                             (AssyHistory, "customer_code"), (Material, "material_code"), (Assy, "customer_code")]:
            total += model.objects.filter(**{f"{field}__startswith": P}).delete()[0]
        SystemStatus.mark_data_changed()
        self.stdout.write(self.style.SUCCESS(f"Demo data deleted ({total} rows). Upload/Recalculate history is kept."))
