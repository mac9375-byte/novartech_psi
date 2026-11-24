"""Safety Stock 테스트 (Ⅵ-4 Acceptance Criteria)."""
import io

from django.test import TestCase
from openpyxl import load_workbook

from accounts.models import UserClass
from core.models import UploadBatch
from core.testutil import assy, upload, user

from .models import SafetyHistory, SafetyStock

H = ["Customer Code", "Safety Q'ty"]


class SafetyTests(TestCase):
    def setUp(self):
        self.client.force_login(user("admin1"))
        assy("A1")
        assy("A2", status="INACTIVE")

    def up(self, rows, apply=True):
        return upload(self.client, "/safety-stock/", {"SAFETY": [H, *rows]}, apply=apply)

    def test_1_full_replace_with_history(self):
        self.up([["A1", 100], ["A2", 50]])
        b = self.up([["a1", 120], ["NEW1", None]])
        self.assertEqual((b.summary["changed"], b.summary["new"], b.summary["deleted"]), (1, 1, 1))
        self.assertEqual(dict(SafetyStock.objects.values_list("customer_code", "qty")), {"A1": 120, "NEW1": 0})
        self.assertEqual(list(SafetyHistory.objects.filter(customer_code="A2").values_list("change_type", flat=True)),
                         ["Add", "Delete"])

    def test_2_3_duplicates_and_invalid_qty_block_upload(self):
        b = self.up([["A1", 1], ["a1", 2], ["X", 1.5], ["Y", -1], ["Z", "abc"]], apply=False)
        self.assertEqual(b.state, UploadBatch.State.FAILED)
        self.assertEqual([i["row"] for i in b.issues if i["level"] == "Error"], [3, 4, 5, 6])

    def test_4_warnings_no_db_inactive_no_bom(self):
        b = self.up([["A2", 10], ["ZZ", 5]])
        reasons = " ".join(i["reason"] for i in b.issues if i["level"] == "Warning")
        for text in ("No DB", "Inactive", "No BOM"):
            self.assertIn(text, reasons)
        self.assertEqual(b.state, UploadBatch.State.APPLIED)

    def test_5_same_content_no_history(self):
        self.up([["A1", 100]])
        self.up([["A1", 100]])
        self.assertEqual(SafetyHistory.objects.count(), 1)

    def test_screen_filter_sort_and_downloads(self):
        self.up([["A2", 10], ["A1", 20], ["ZZ", 5]])
        page = self.client.get("/safety-stock/")
        self.assertContains(page, ">A1<")
        self.assertNotContains(page, ">A2<")
        self.assertContains(self.client.get("/safety-stock/", {"status": "NODB"}), ">ZZ<")
        ws = load_workbook(io.BytesIO(self.client.get("/safety-stock/download.xlsx", {"status": "ALL"}).content))["SAFETY"]
        self.assertEqual([ws.cell(r, 2).value for r in (2, 3, 4)], ["A1", "A2", "ZZ"])
        self.assertNotContains(page, 'name="sel"')

    def test_8_non_admin_cannot_upload(self):
        self.client.force_login(user("u1", UserClass.USER))
        self.assertEqual(self.client.post("/safety-stock/upload/").status_code, 403)
