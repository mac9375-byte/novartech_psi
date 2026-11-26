"""Module 9·10 계산·Recalculate·Weekly Reset 테스트 (Ⅲ-4, Ⅵ-9, Ⅵ-10, Ⅳ-7)."""
from datetime import date
from decimal import Decimal
from fractions import Fraction as F

from django.test import SimpleTestCase, TestCase

from accounts.models import User, UserClass
from bom.models import BomLine, BomVersion
from core import weeks
from core.models import OperationLog, SystemStatus
from core.testutil import assy, material, user
from materials.models import Material, UnitCode
from safety.models import SafetyStock
from weekly.models import InventoryRow, OpenPoRow, PlanRow, SchedRow

from . import engine
from .models import MrRow, PsiRow

W = weeks.current_week()
D = Decimal


def bom(code, lines, u):
    v = BomVersion.objects.create(customer_code=code, updated_by=u)
    for i, (mat, unit, num, den) in enumerate(lines, start=1):
        BomLine.objects.create(version=v, seq=i, material_code=mat, unit=unit, qty_num=num, qty_den=den)


class CalcTests(TestCase):
    """예시: Material M(EA, L/T 8), Assy A BOM: M 2개 (1 + 1 두 행). RTF 100/주 + Safety 50, Prod. 10/주.
    재고 M 5,000, Assy A 1,000. Open PO 11,000 (In Transit 1,000 + Remain 10,000). 입고예정 W0 3,000."""

    def setUp(self):
        self.admin = user("admin1")
        self.client.force_login(self.admin)
        material("M", "EA", lt=8, desc="Magnet")
        assy("A")
        bom("A", [("M", "EA", 1, 1), ("M", "EA", 1, 1)], self.admin)
        SafetyStock.objects.create(customer_code="A", qty=50, updated_by=self.admin)
        PlanRow.objects.create(week=W, plan="RTF", customer_code="A", qty=[100] * 14)
        PlanRow.objects.create(week=W, plan="PROD", customer_code="A", qty=[10] * 14)
        InventoryRow.objects.create(week=W, category="MATERIAL", code="M", unit="EA", qty=5000)
        InventoryRow.objects.create(week=W, category="ASSY", code="A", unit="EA", qty=1000)
        OpenPoRow.objects.create(week=W, seq=1, po_date=date(2026, 6, 1), po_no="P1", material_code="M", unit="EA",
                                 po_qty=12000, gr=1000, in_transit=1000, vendor="YX")
        SchedRow.objects.create(week=W, material_code="M", vendor="YX", vendor_key="YX", unit="EA",
                                qty=["3000"] + ["0"] * 13)

    def recalc(self):
        return self.client.post("/material-psi/recalculate/", follow=True)

    def psi(self, plan):
        return PsiRow.objects.get(week=W, plan=plan, material_code="M")

    def test_requirement_and_psi_formulas(self):
        self.assertEqual(MrRow.objects.count(), 0)             # 재계산 전에는 빈칸 (작동 예 1)
        r = self.recalc()
        self.assertContains(r, "재계산이 완료되었습니다")
        total = MrRow.objects.get(week=W, plan="RTF", material_code="M", customer_code="")
        self.assertEqual((D(total.values[0]), D(total.values[13])), (200, 300))   # 14주차 = (100 + 50) × 2
        assy_row = MrRow.objects.get(week=W, plan="RTF", material_code="M", customer_code="A")
        self.assertEqual(assy_row.qty, 2)                       # 같은 자재 두 행 합산 표시 (M-1)
        prod = MrRow.objects.get(week=W, plan="PROD", material_code="M", customer_code="")
        self.assertEqual(D(prod.values[13]), 20)                # Prod.에는 Safety 미반영

        rtf = self.psi("RTF")
        self.assertEqual((rtf.opening, rtf.open_po), (7000, 11000))              # 5,000 + 1,000 × 2
        self.assertEqual(D(rtf.sr_manual[0]), 3000)
        self.assertEqual(D(rtf.sr_calc[8]), 8000)                                 # 11,000 − 3,000 → W+8
        self.assertEqual(D(rtf.inv_balance[0]), 9800)                             # 7,000 + 3,000 − 200
        self.assertEqual(D(rtf.po_balance[0]), 17800)                             # 7,000 + 11,000 − 200
        self.assertEqual(D(rtf.inv_balance[1]), 9600)
        p = self.psi("PROD")
        self.assertEqual((p.opening, D(p.inv_balance[0]), D(p.po_balance[0])), (5000, 7980, 15980))
        self.assertFalse(SystemStatus.get().need_recalculation)

        page = self.client.get("/material-psi/")
        self.assertContains(page, "Inventory Balance")
        self.assertContains(page, "9,800")
        self.assertContains(self.client.get("/material-requirement/"), ">Total<")

    def test_negative_balance_highlighted(self):
        InventoryRow.objects.filter(week=W).delete()
        SchedRow.objects.all().delete()
        OpenPoRow.objects.all().delete()
        self.recalc()
        self.assertEqual(D(self.psi("RTF").inv_balance[0]), -200)
        self.assertContains(self.client.get("/material-psi/"), "negcell")

    def test_need_recalculation_shows_button_on_module_pages_for_admin_only(self):
        SystemStatus.mark_data_changed()
        btn = 'action="/material-psi/recalculate/"'
        self.assertContains(self.client.get("/material-master/"), btn)
        self.client.force_login(user("viewer1", UserClass.USER))
        self.assertNotContains(self.client.get("/material-master/"), btn)

    def test_order_requirement_row(self):
        """재고·PO 없음: RTF 소요 200/주(14주차 300), L/T 8 → W0~W8 부족분은 늦어서 W0 합산(Overdue)."""
        InventoryRow.objects.filter(week=W).delete()
        SchedRow.objects.all().delete()
        OpenPoRow.objects.all().delete()
        Material.objects.filter(material_code="M").update(safety_stock=0, moq=0)
        self.recalc()
        o = [D(x) for x in self.psi("RTF").order_req]
        self.assertEqual((o[0], o[1], o[4], o[5], sum(o)), (1800, 200, 200, 300, 2900))
        page = self.client.get("/material-psi/")
        self.assertContains(page, "Order Requirement")
        self.assertContains(page, "Overdue")

    def test_no_bom_and_safety_only_auto_generation_warnings(self):
        assy("B")
        PlanRow.objects.create(week=W, plan="RTF", customer_code="B", qty=[5] * 14)   # BOM 없음
        SafetyStock.objects.create(customer_code="S", qty=7, updated_by=self.admin)    # Safety에만 있음
        self.recalc()
        log = OperationLog.objects.get(kind="RECALC")
        self.assertEqual(log.details["no_bom"], 2)          # B, 그리고 Safety만 있고 BOM 없는 S
        self.assertGreaterEqual(log.details["auto_generated"], 2)
        self.assertTrue(PlanRow.objects.filter(week=W, customer_code="S", auto=True).count() == 2)
        page = self.client.get("/material-requirement/")
        self.assertContains(page, "BOM 미등록 Assy 2건")

    def test_bom_unit_mismatch_blocks_and_keeps_previous_results(self):
        self.recalc()
        before = list(PsiRow.objects.values_list("id", flat=True))
        Material.objects.filter(material_code="M").update(unit=UnitCode.objects.get(code="KG"))
        r = self.recalc()
        self.assertContains(r, "Recalculation failed")
        self.assertEqual(list(PsiRow.objects.values_list("id", flat=True)), before)

    def test_inactive_and_no_db_are_included(self):
        Material.objects.filter(material_code="M").update(status="INACTIVE")
        PlanRow.objects.create(week=W, plan="RTF", customer_code="NODB", qty=[1] * 14)
        bom("NODB", [("M", "EA", 1, 1)], self.admin)
        self.recalc()
        total = MrRow.objects.get(week=W, plan="RTF", material_code="M", customer_code="")
        self.assertEqual(D(total.values[0]), 201)
        warnings = " ".join(OperationLog.objects.get(kind="RECALC").details["warnings"])
        self.assertIn("Inactive", warnings)
        self.assertIn("No DB", warnings)

    def test_weekly_reset_clears_only_current_week_5_to_8(self):
        past = weeks.add_weeks(W, -1)
        InventoryRow.objects.create(week=past, category="MATERIAL", code="M", unit="EA", qty=1)
        self.recalc()
        r = self.client.post("/material-psi/weekly-reset/", follow=True)
        self.assertContains(r, "Upload new weekly data in this week.")
        for m in (InventoryRow, PlanRow, OpenPoRow, SchedRow):
            self.assertFalse(m.objects.filter(week=W).exists())
        self.assertTrue(InventoryRow.objects.filter(week=past).exists())
        self.assertTrue(SafetyStock.objects.exists())
        self.assertTrue(PsiRow.objects.filter(week=W).exists())   # Recalculate 전까지 결과 유지 (작동 예 2)
        self.assertTrue(SystemStatus.get().need_recalculation)

    def test_only_admin_can_recalculate_or_reset(self):
        for cls in (UserClass.MASTER, UserClass.USER, UserClass.GUEST):
            self.client.force_login(user(f"u{cls.lower()}", cls))
            self.assertEqual(self.client.post("/material-psi/recalculate/").status_code, 403)
            self.assertEqual(self.client.post("/material-psi/weekly-reset/").status_code, 403)
            self.assertContains(self.client.get("/material-psi/"), "Material PSI")
        self.assertFalse(OperationLog.objects.exists())

    def test_past_week_snapshot_and_downloads(self):
        self.recalc()
        self.assertEqual(self.client.get("/material-psi/download.xlsx").status_code, 200)
        self.assertEqual(self.client.get("/material-requirement/download.xlsx").status_code, 200)
        self.assertEqual(self.client.get("/material-psi/log.xlsx").status_code, 200)
        page = self.client.get("/material-psi/", {"week": weeks.add_weeks(W, -1)})
        self.assertContains(page, "No data.")


class OrderRequirementFormulaTests(SimpleTestCase):
    """발주필요수량 (v1.1): PO 과부족 − 자재 안전재고가 음수인 주차의 부족분을 L/T만큼 앞당겨 발주 주차에 표시."""

    def calc(self, po, ss=0, moq=0, lt=1, rounding=0):
        po = [F(x) for x in po] + [F(po[-1])] * (14 - len(po))
        return engine.order_requirement(po, ss, moq, lt, rounding)

    def test_no_shortage_is_all_zero(self):
        self.assertEqual(self.calc([100] * 14), ([0] * 14, 0))

    def test_shortage_netted_week_by_week_and_released_lt_earlier(self):
        rel, overdue = self.calc([100, 50, -30, -80], lt=1)
        self.assertEqual((rel[1], rel[2], sum(rel), overdue), (30, 50, 80, 0))

    def test_below_moq_rounds_up_to_moq_and_covers_later_weeks(self):
        rel, _ = self.calc([100, 50, -30, -80], moq=100, lt=1)
        self.assertEqual((rel[1], sum(rel)), (100, 100))

    def test_material_safety_stock_and_fraction_rounded_up(self):
        rel, overdue = self.calc([F(-1, 2)], ss=10, lt=1)
        self.assertEqual((rel[0], overdue), (11, 11))           # 0.5 + 10 → 11, 이미 늦어 W0

    def test_rounding_value_applied_after_moq(self):
        rel, _ = self.calc([0, 0, -3000, -15300], moq=10000, rounding=5000, lt=1)
        self.assertEqual((rel[1], rel[2], sum(rel)), (10000, 10000, 20000))   # 3,000→MOQ 10,000 / 5,300→10,000
        rel, _ = self.calc([0, -12300], moq=10000, rounding=5000, lt=1)
        self.assertEqual(rel[0], 15000)                                       # 12,300 → 5,000 배수 15,000
        rel, _ = self.calc([0, -100], moq=12000, rounding=5000, lt=1)
        self.assertEqual(rel[0], 15000)                                       # MOQ 먼저, 그 다음 배수 올림

    def test_release_before_w0_is_overdue_at_w0(self):
        rel, overdue = self.calc([0, 0, -40, -40], lt=8)
        self.assertEqual((rel[0], overdue, sum(rel)), (40, 40, 40))
