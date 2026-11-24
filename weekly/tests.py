"""Module 5~8 테스트 (Ⅵ-5 ~ Ⅵ-8 Acceptance Criteria)."""
import io
from datetime import date
from decimal import Decimal

from django.test import TestCase
from openpyxl import load_workbook

from accounts.models import UserClass
from core import weeks
from core.models import UploadBatch
from core.testutil import assy, material, upload, user

from .models import InventoryRow, OpenPoRow, PlanRow, SchedRow
from .services import scheduled_receipts

W = weeks.current_week()
HZ = weeks.horizon(W)
PO_H = ["PO Date", "PO No", "Material Code", "Unit", "PO Q'ty", "Currency", "Unit Price", "Cancel", "G/R",
        "In Transit", "Vendor"]


def po(mat, qty, cancel=0, gr=0, it=0, vendor="YX", unit="EA", price=None, cur=None, no="PO-1"):
    return [date(2026, 7, 1), no, mat, unit, qty, cur, price, cancel, gr, it, vendor]


class Base(TestCase):
    def setUp(self):
        self.client.force_login(user("admin1"))
        material("M1", "EA", lt=8)
        material("M2", "KG", lt=2)
        assy("A1")

    def up(self, prefix, sheets, apply=True):
        return upload(self.client, prefix, sheets, apply=apply)


class InventoryTests(Base):
    H = ["Category", "Code", "Unit", "Stock Q'ty"]

    def test_replace_week_and_rules(self):
        InventoryRow.objects.create(week=weeks.add_weeks(W, -1), category="MATERIAL", code="OLD", unit="EA", qty=1)
        b = self.up("/inventory/", {"INVENTORY": [self.H, ["Assy", "a1", None, 500], ["material", "M2", "kg", 0.5],
                                                  ["Material", "NEW", "EA", None]]})
        self.assertEqual(b.state, UploadBatch.State.APPLIED)
        rows = {(r.category, r.code): (r.unit, r.qty) for r in InventoryRow.objects.filter(week=W)}
        self.assertEqual(rows, {("ASSY", "A1"): ("EA", 500), ("MATERIAL", "M2"): ("KG", Decimal("0.5")),
                                ("MATERIAL", "NEW"): ("EA", 0)})
        self.assertTrue(InventoryRow.objects.filter(code="OLD").exists())   # 과거 주차 보존
        b = self.up("/inventory/", {"INVENTORY": [self.H, ["Assy", "A1", None, 1]]})
        self.assertEqual(InventoryRow.objects.filter(week=W).count(), 1)      # 전체교체

    def test_errors(self):
        b = self.up("/inventory/", {"INVENTORY": [self.H, ["Assy", "A1", "SET", 1], ["Material", "M1", "KG", 1],
                                                  ["Material", "M2", "KG", -1], ["Material", "M2", "KG", "0.1234567"],
                                                  ["Box", "X", "EA", 1], ["Assy", "B1", "", 1], ["assy", "b1", "", 2]]},
                    apply=False)
        self.assertEqual([i["row"] for i in b.issues if i["level"] == "Error"], [2, 3, 4, 5, 6, 8])

    def test_past_week_upload_disabled(self):
        page = self.client.get("/inventory/", {"week": weeks.add_weeks(W, -1)})
        self.assertContains(page, 'id="open-upload" disabled')
        self.assertContains(page, "Past week")


class PlanTests(Base):
    def sheet(self, plan, rows):
        return [["Customer Code", "Plan", *HZ], *[[c, plan, *q] for c, q in rows]]

    def test_rtf_only_creates_prod_zero_and_safety_shown(self):
        from safety.models import SafetyStock
        from accounts.models import User
        SafetyStock.objects.create(customer_code="A1", qty=500, updated_by=User.objects.first())
        q = [10] * 14
        b = self.up("/rtf-production/", {"RTF": self.sheet("RTF", [("A1", q), ("B1", q)])})
        self.assertEqual(b.state, UploadBatch.State.APPLIED)
        prod = PlanRow.objects.get(week=W, plan="PROD", customer_code="A1")
        self.assertEqual((prod.auto, prod.qty), (True, [0] * 14))
        page = self.client.get("/rtf-production/")
        self.assertContains(page, "Safety(W+13)")
        self.assertContains(page, ">510<")       # RTF 14주차 = 10 + Safety 500
        self.assertContains(page, ">NO<")        # BOM 미등록
        ws = load_workbook(io.BytesIO(self.client.get("/rtf-production/download.xlsx").content))["RTF"]
        self.assertEqual(ws.cell(2, 16).value, 10)   # Download는 원본값 (Safety 제외)

    def test_prod_upload_replaces_only_prod(self):
        self.up("/rtf-production/", {"RTF": self.sheet("RTF", [("A1", [1] * 14)])})
        self.up("/rtf-production/", {"PROD_PLAN": self.sheet("Prod.", [("A1", [2] * 14)])})
        self.assertEqual(PlanRow.objects.get(week=W, plan="RTF", customer_code="A1").qty, [1] * 14)
        p = PlanRow.objects.get(week=W, plan="PROD", customer_code="A1")
        self.assertEqual((p.qty, p.auto), ([2] * 14, False))

    def test_errors(self):
        rows = [["A1", "Prod.", *[1] * 14], ["B1", "RTF", -1, *[0] * 13], ["C1", "RTF", 1.5, *[0] * 13],
                ["c1", "RTF", *[0] * 14]]
        b = self.up("/rtf-production/", {"RTF": [["Customer Code", "Plan", *HZ], *rows]}, apply=False)
        self.assertEqual([i["row"] for i in b.issues if i["level"] == "Error"], [2, 3, 4, 5])   # 5: 중복 Code
        wrong = [weeks.add_weeks(w, 1) for w in HZ]
        b = self.up("/rtf-production/", {"RTF": [["Customer Code", "Plan", *wrong], ["A1", "RTF", *[0] * 14]]}, apply=False)
        self.assertIn("14 consecutive weeks", " ".join(i["reason"] for i in b.issues))
        b = self.up("/rtf-production/", {"OTHER": [["x"]]}, apply=False)
        self.assertEqual(b.state, UploadBatch.State.FAILED)


class OpenPoSchedTests(Base):
    def test_open_po_rules_and_calculated_receipt(self):
        b = self.up("/open-po/", {"OPEN_PO": [PO_H, po("M1", 50000, cancel=10000, gr=20000, it=5000, price=0.75, cur="USD"),
                                              po("M1", 100, gr=100, no="PO-2"),
                                              po("M1", 30, gr=0, it=30, no="PO-3")]})
        self.assertEqual(b.state, UploadBatch.State.APPLIED)
        r = OpenPoRow.objects.get(po_no="PO-1")
        self.assertEqual((r.final_po, r.remain, r.open_qty, r.amount), (40000, 15000, 20000, Decimal("37500")))
        page = self.client.get("/open-po/")
        self.assertContains(page, "37,500")
        # Manual 입고예정 3,000 → 차이분 20,030 − 3,000 = 17,030 을 W0 + L/T 8주에 파랑 표시
        b = self.up("/scheduled-receipt/", {"SCHED_RECEIPT": [["Material Code", "Vendor", "Unit", *HZ],
                                                              ["M1", " yx ", "EA", 3000, *[None] * 13]]})
        self.assertEqual(b.state, UploadBatch.State.APPLIED)
        it = scheduled_receipts(W)[("M1", "YX")]
        self.assertEqual((it["manual"][0], it["calc"][8], it["diff"]), (3000, 17030, 17030))
        self.assertContains(self.client.get("/scheduled-receipt/"), "17,030")

    def test_open_po_errors(self):
        b = self.up("/open-po/", {"OPEN_PO": [PO_H, po("M1", 10, gr=11), po("M1", 10, unit="KG"),
                                              po("M1", 10, price=1), po("M1", 0), [None, "x", "M1", "EA", 1, None,
                                                                                    None, 0, 0, 0, "V"]]}, apply=False)
        self.assertEqual(sorted({i["row"] for i in b.issues if i["level"] == "Error"}), [2, 3, 4, 5, 6])

    def test_sched_over_open_po_and_duplicate_errors(self):
        self.up("/open-po/", {"OPEN_PO": [PO_H, po("M1", 100)]})
        b = self.up("/scheduled-receipt/", {"SCHED_RECEIPT": [["Material Code", "Vendor", "Unit", *HZ],
                                                              ["M1", "YX", "EA", 101, *[0] * 13],
                                                              ["M2", "NOPO", "KG", 1, *[0] * 13]]}, apply=False)
        self.assertEqual(b.error_count, 2)                      # 둘 다 Open PO 초과 (M2는 Open PO 없음 = 0)
        b = self.up("/scheduled-receipt/", {"SCHED_RECEIPT": [["Material Code", "Vendor", "Unit", *HZ],
                                                              ["M1", "YX", "EA", 1, *[0] * 13],
                                                              ["M1", "yx", "EA", 1, *[0] * 13]]}, apply=False)
        self.assertIn("Duplicate Material + Vendor", b.issues[0]["reason"])

    def test_lead_time_beyond_horizon_goes_to_last_week(self):
        material("M9", "EA", lt=20)
        self.up("/open-po/", {"OPEN_PO": [PO_H, po("M9", 7)]})
        self.assertEqual(scheduled_receipts(W)[("M9", "YX")]["calc"][13], 7)

    def test_no_db_material_skips_calculation(self):
        self.up("/open-po/", {"OPEN_PO": [PO_H, po("NODB1", 7)]})
        it = scheduled_receipts(W)[("NODB1", "YX")]
        self.assertTrue(it["skipped"])
        self.assertEqual(sum(it["calc"]), 0)

    def test_guest_cannot_upload(self):
        self.client.force_login(user("g1", UserClass.GUEST))
        self.assertEqual(self.client.post("/open-po/upload/").status_code, 403)
        self.assertEqual(self.client.get("/open-po/").status_code, 200)
