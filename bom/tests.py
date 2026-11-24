"""BOM 테스트 (Ⅵ-3 Acceptance Criteria)."""
import io
from datetime import datetime
from fractions import Fraction

from django.test import TestCase
from openpyxl import load_workbook

from accounts.models import UserClass
from core.models import UploadBatch
from core.testutil import assy, material, upload, user

from . import services as svc
from .models import BomVersion

H = ["Customer Code", "Material Code", "Unit", "Q'ty"]


class BomTests(TestCase):
    def setUp(self):
        self.client.force_login(user("admin1"))
        material("M1", "EA", desc="Magnet")
        material("M2", "G")
        assy("A1")

    def up(self, rows, t="CHANGE", apply=True):
        return upload(self.client, "/bom/", {"BOM": [H, *rows]}, t, apply)

    def lines(self, code):
        v = BomVersion.objects.get(customer_code=code, is_current=True)
        return [(l.material_code, l.unit, l.qty) for l in v.lines.all()]

    def test_1_assy_row_marks_block_and_its_unit_qty_ignored(self):
        b = self.up([["a1", "assy", "XX", "abc"], ["A1", "m1", "ea", 1], ["A1", "M2", "G", "1/200"],
                     ["A1", "M1", "EA", 0.3]])
        self.assertEqual(b.state, UploadBatch.State.APPLIED)
        self.assertEqual(self.lines("A1"), [("M1", "EA", 1), ("M2", "G", Fraction(1, 200)), ("M1", "EA", Fraction(3, 10))])
        self.assertEqual(svc.bom_map()["A1"]["M1"], Fraction(13, 10))  # 같은 자재 여러 행은 계산 시 합산

    def test_2_3_no_db_codes_allowed_with_warning(self):
        b = self.up([["ZZ", "Assy"], ["ZZ", "NEWMAT", "SET", 2]])
        self.assertEqual(b.state, UploadBatch.State.APPLIED)
        self.assertEqual(sorted(i["field"] for i in b.issues if i["level"] == "Warning"), ["Customer Code", "Material Code"])
        page = self.client.get("/bom/", {"status": "NODB"})
        self.assertContains(page, "No DB")

    def test_4_assy_code_as_material_and_structure_errors(self):
        b = self.up([["A1", "Assy"], ["A1", "M1", "EA", 1], ["B1", "Assy"], ["B1", "M1", "EA", 1],
                     ["A1", "M2", "G", 1], ["C1", "M1", "EA", 1], ["D1", "Assy"], ["D1", "Assy"]], apply=False)
        reasons = " | ".join(i["reason"] for i in b.issues if i["level"] == "Error")
        self.assertIn("continuous", reasons)
        self.assertIn("must start with an Assy row", reasons)
        self.assertIn("appears twice", reasons)
        self.assertEqual(b.state, UploadBatch.State.FAILED)

    def test_6_unit_mismatch_and_7_qty_errors(self):
        b = self.up([["A1", "Assy"], ["A1", "M1", "G", 1], ["A1", "M2", "G", 0], ["A1", "M2", "G", -1],
                     ["A1", "M2", "G", "x"], ["A1", "M2", "G", datetime(2026, 1, 50 // 50)]], apply=False)
        fields = [(i["row"], i["field"]) for i in b.issues if i["level"] == "Error"]
        self.assertEqual(fields, [(3, "Unit"), (4, "Q'ty"), (5, "Q'ty"), (6, "Q'ty"), (7, "Q'ty")])
        self.assertIn("date", [i for i in b.issues if i["row"] == 7][0]["reason"])
        self.assertFalse(BomVersion.objects.exists())

    def test_9_assy_without_materials_ignored_and_existing_kept(self):
        self.up([["A1", "Assy"], ["A1", "M1", "EA", 1]])
        b = self.up([["A1", "Assy"]])
        self.assertEqual(b.summary["ignored"], 1)
        self.assertEqual(self.lines("A1"), [("M1", "EA", 1)])

    def test_10_11_change_replaces_only_file_assy_and_keeps_history(self):
        assy("B1")
        self.up([["A1", "Assy"], ["A1", "M1", "EA", 1], ["B1", "Assy"], ["B1", "M1", "EA", 2]])
        b = self.up([["A1", "Assy"], ["A1", "M2", "G", "1/50"]])
        self.assertEqual(b.summary["changed"], 1)
        self.assertEqual(self.lines("A1"), [("M2", "G", Fraction(1, 50))])
        self.assertEqual(self.lines("B1"), [("M1", "EA", 2)])
        self.assertEqual(BomVersion.objects.filter(customer_code="A1").count(), 2)
        b = self.up([["A1", "Assy"], ["A1", "M2", "G", 0.02]])     # 같은 내용 → 이력 미생성
        self.assertEqual(b.summary["unchanged"], 1)
        self.assertEqual(BomVersion.objects.filter(customer_code="A1").count(), 2)
        b = self.up([["A1", "Assy"], ["A1", "M1", "EA", 9]], "ADD")  # Add는 기존 Assy 무시
        self.assertEqual(b.summary["skipped"], 1)

    def test_screen_search_status_fraction_and_downloads(self):
        assy("B1", status="INACTIVE")
        self.up([["A1", "Assy"], ["A1", "M2", "G", "1/1000"], ["B1", "Assy"], ["B1", "M1", "EA", 1]])
        page = self.client.get("/bom/")
        self.assertContains(page, "1/1,000")
        self.assertNotContains(page, ">B1<")
        page = self.client.get("/bom/", {"status": "ALL", "field": "mat", "q": "m1"})
        self.assertContains(page, ">B1<")
        self.assertNotContains(page, ">A1<")
        ws = load_workbook(io.BytesIO(self.client.get("/bom/download.xlsx", {"status": "ALL"}).content))["BOM"]
        self.assertEqual([c.value for c in ws[2]][:2], ["A1", "Assy"])
        self.assertEqual(ws.cell(3, 6).value, "1/1000")
        self.up([["A1", "Assy"], ["A1", "M1", "EA", 3]])
        hist = load_workbook(io.BytesIO(self.client.get("/bom/history.xlsx", {"q": "A1"}).content))["History"]
        versions = [r[10].value for r in hist.iter_rows(min_row=2)]
        self.assertEqual(versions, ["History", "History", "Current", "Current"])

    def test_17_upload_admin_only(self):
        self.client.force_login(user("g1", UserClass.GUEST))
        self.assertEqual(self.client.post("/bom/upload/", {"upload_type": "ADD"}).status_code, 403)
        self.assertEqual(self.client.get("/bom/").status_code, 200)
