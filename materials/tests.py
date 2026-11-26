"""Material Master 테스트 (설계/01 B-15, 설계/03 6절)."""
import io

import psycopg
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import connection
from django.test import TestCase, TransactionTestCase
from openpyxl import Workbook, load_workbook

from accounts.models import IdStatus, User, UserClass
from core.models import SystemStatus, UploadBatch

from .models import Material, MaterialHistory, Status

HEADERS = ["Material Code", "Desc.", "Spec.", "Unit", "Purchaser ID", "Vendor", "Country", "L/T(Weeks)"]


def xlsx_file(rows, headers=HEADERS, sheet="MD_Material", name="m.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = sheet
    ws.append(headers)
    for r in rows:
        ws.append(r)
    buf = io.BytesIO()
    wb.save(buf)
    return SimpleUploadedFile(name, buf.getvalue())


def row(code, desc="Magnet", unit="EA", purchaser="nova007", lt=5, spec="d7", vendor="KS", country="Korea"):
    return [code, desc, spec, unit, purchaser, vendor, country, lt]


class Base(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user("admin1", "abcd1234", name="Admin", email="a@t.local",
                                              user_class=UserClass.ADMIN, id_status=IdStatus.APPROVED)
        self.buyer = User.objects.create_user("nova007", "abcd1234", name="Emily", email="e@t.local",
                                              id_status=IdStatus.APPROVED)
        self.client.force_login(self.admin)

    def upload(self, rows, upload_type="CHANGE", **kw):
        r = self.client.post("/material-master/upload/", {"upload_type": upload_type, "file": xlsx_file(rows, **kw)})
        return UploadBatch.objects.latest("id"), r

    def upload_apply(self, rows, upload_type="CHANGE", **kw):
        batch, _ = self.upload(rows, upload_type, **kw)
        self.client.post(f"/material-master/upload/{batch.pk}/apply/")
        batch.refresh_from_db()
        return batch

    def mat(self, code):
        return Material.objects.get(material_code=code)


class UploadTests(Base):
    def test_1_add_registers_new_and_skips_existing(self):
        self.upload_apply([row("A1"), row("A2")], "ADD")
        batch = self.upload_apply([row("A1", desc="NEW"), row("A2"), row("A3"), row("A4"), row("A5")], "ADD")
        s = batch.summary
        self.assertEqual((s["new"], s["skipped"]), (3, 2))
        self.assertEqual(Material.objects.count(), 5)
        self.assertEqual(self.mat("A1").description, "Magnet")  # Add는 기존값 무시

    def test_2_change_updates_reactivates_and_blank_becomes_null(self):
        self.upload_apply([row("A1"), row("A2")])
        Material.objects.filter(material_code="A2").update(status=Status.INACTIVE)
        batch, _ = self.upload([row("A1", desc=None, lt=8), row("A2"), row("A3")])
        s = batch.summary
        self.assertEqual((s["changed"], s["reactivated"], s["new"]), (1, 1, 1))
        changes = {d["code"]: d["changes"] for d in s["details"]}
        self.assertIn("L/T(Weeks): 5 → 8", changes["A1"])
        self.client.post(f"/material-master/upload/{batch.pk}/apply/")
        a1 = self.mat("A1")
        self.assertEqual((a1.description, a1.lead_time_weeks, a1.version), (None, 8, 2))
        self.assertEqual(self.mat("A2").status, Status.ACTIVE)

    def test_3_inactive_upload_uses_code_only(self):
        self.upload_apply([row("A1"), row("A2")])
        batch = self.upload_apply([["a1"], ["A2"], ["NOPE"]], "INACTIVE", headers=["Material Code"])
        self.assertEqual((batch.summary["inactive"], batch.summary["skipped"]), (2, 1))
        self.assertEqual(self.mat("A1").status, Status.INACTIVE)

    def test_4_duplicate_code_after_normalization_blocks_whole_upload(self):
        batch, _ = self.upload([row("smaz13001"), row("SMAZ13001 ")])
        self.assertEqual(batch.state, UploadBatch.State.FAILED)
        self.assertIn("Duplicate", batch.issues[0]["reason"])
        self.client.post(f"/material-master/upload/{batch.pk}/apply/")
        self.assertEqual(Material.objects.count(), 0)

    def test_5_lead_time_rules(self):
        batch, _ = self.upload([row("A1", lt=0), row("A2", lt=1.5), row("A3", lt=None), row("A4", lt="5")])
        bad_rows = sorted(i["row"] for i in batch.issues if i["field"] == "L/T(Weeks)")
        self.assertEqual(bad_rows, [2, 3, 4])

    def test_6_unit_rules_upper_case_and_required(self):
        batch = self.upload_apply([row("A1", unit="sheet")])
        self.assertEqual(self.mat("A1").unit_id, "SHEET")
        batch, _ = self.upload([row("A2", unit="BOX"), row("A3", unit=None)])
        self.assertEqual(sorted(i["row"] for i in batch.issues if i["field"] == "Unit"), [2, 3])

    def test_7_numeric_code_kept_as_text_and_exponent_is_error(self):
        self.upload_apply([row(4605000219)])
        self.assertTrue(Material.objects.filter(material_code="4605000219").exists())
        batch, _ = self.upload([row("3.04E+11")])
        self.assertIn("Exponent", batch.issues[0]["reason"])

    def test_assy_code_and_unknown_purchaser_are_errors(self):
        batch, _ = self.upload([row("assy"), row("A1", purchaser="ghost")])
        self.assertEqual(sorted(i["field"] for i in batch.issues if i["level"] == "Error"), ["Material Code", "Purchaser ID"])

    def test_purchaser_id_is_case_insensitive(self):
        self.upload_apply([row("A1", purchaser="NOVA007")])
        self.assertEqual(self.mat("A1").purchaser, self.buyer)

    def test_unchanged_rows_keep_update_time_and_history(self):
        self.upload_apply([row("A1")])
        before = self.mat("A1").updated_at
        batch = self.upload_apply([row("A1")])
        self.assertEqual(batch.summary["unchanged"], 1)
        self.assertEqual(self.mat("A1").updated_at, before)
        self.assertEqual(MaterialHistory.objects.count(), 1)

    def test_apply_rejected_when_data_changed_after_preview(self):
        batch, _ = self.upload([row("A1")])
        self.upload_apply([row("A2")])  # 다른 Upload가 먼저 반영
        self.client.post(f"/material-master/upload/{batch.pk}/apply/")
        batch.refresh_from_db()
        self.assertEqual(batch.state, UploadBatch.State.PREVIEW)
        self.assertFalse(Material.objects.filter(material_code="A1").exists())

    def test_upload_marks_need_recalculation(self):
        self.upload_apply([row("A1")])
        self.assertTrue(SystemStatus.get().need_recalculation)
        self.assertContains(self.client.get("/material-master/"), "Need Recalculation")

    def test_wrong_sheet_name(self):
        batch, _ = self.upload([row("A1")], sheet="Sheet1")
        self.assertEqual(batch.issues[0]["field"], "Sheet")


class ScreenTests(Base):
    def setUp(self):
        super().setUp()
        self.upload_apply([row("A1"), row("B2", vendor="YX")])
        self.m = self.mat("A1")

    def post_save(self, m, **over):
        data = {"sel": [m.pk], f"version_{m.pk}": m.version, f"desc_{m.pk}": m.description or "",
                f"spec_{m.pk}": m.spec or "", f"unit_{m.pk}": m.unit_id, f"purchaser_{m.pk}": "nova007",
                f"vendor_{m.pk}": m.vendor or "", f"country_{m.pk}": m.country or "",
                f"lt_{m.pk}": m.lead_time_weeks, f"status_{m.pk}": m.status}
        data.update({f"{k}_{m.pk}": v for k, v in over.items()})
        return self.client.post("/material-master/save/", data, follow=True)

    def test_save_selected_row_and_history(self):
        self.post_save(self.m, desc="Holder", lt=7)
        m = self.mat("A1")
        self.assertEqual((m.description, m.lead_time_weeks, m.version), ("Holder", 7, 2))
        self.assertEqual(MaterialHistory.objects.filter(material_code="A1").last().change_type, "Screen")

    def test_8_optimistic_lock_conflict(self):
        Material.objects.filter(pk=self.m.pk).update(version=5)
        r = self.post_save(self.m, desc="X")
        self.assertContains(r, "Another user changed this data first")
        self.assertEqual(self.mat("A1").description, "Magnet")

    def test_inactive_via_screen_and_status_filter(self):
        self.post_save(self.m, status="INACTIVE")
        self.assertEqual(self.mat("A1").status, Status.INACTIVE)
        self.assertNotContains(self.client.get("/material-master/"), ">A1<")
        self.assertContains(self.client.get("/material-master/?status=INACTIVE"), ">A1<")

    def test_invalid_screen_values_are_rejected(self):
        r = self.post_save(self.m, lt="0", unit="BOX")
        self.assertContains(r, "L/T(Weeks) must be")
        self.assertEqual(self.mat("A1").lead_time_weeks, 5)

    def test_9_non_admin_cannot_save_or_upload(self):
        for cls in [UserClass.MASTER, UserClass.USER, UserClass.GUEST]:
            u = User.objects.create_user(f"u{cls.lower()}", "abcd1234", name="x", email="x@t.local",
                                         user_class=cls, id_status=IdStatus.APPROVED)
            self.client.force_login(u)
            self.assertEqual(self.client.post("/material-master/save/", {"sel": [self.m.pk]}).status_code, 403)
            self.assertEqual(self.client.post("/material-master/upload/", {"upload_type": "ADD"}).status_code, 403)
            page = self.client.get("/material-master/")
            self.assertEqual(page.status_code, 200)
            self.assertNotContains(page, 'name="desc_')  # 수정 입력칸 없음

    def test_10_search_download_and_history(self):
        self.buyer.name = "Emily Kim"
        self.buyer.save()
        r = self.client.get("/material-master/", {"status": "ALL", "field": "purchaser", "q": "emi"})
        self.assertContains(r, ">A1<")
        r = self.client.get("/material-master/", {"field": "vendor", "q": "yx"})
        self.assertNotContains(r, ">A1<")
        self.assertContains(r, ">B2<")

        wb = load_workbook(io.BytesIO(self.client.get("/material-master/download.xlsx", {"field": "vendor", "q": "yx"}).content))
        ws = wb["MD_Material"]
        self.assertEqual([c.value for c in ws[1]][:3], ["No", "Material Code", "Desc."])
        self.assertEqual(ws.max_row, 2)

        self.post_save(self.m, desc="Holder")
        wb = load_workbook(io.BytesIO(self.client.get("/material-master/history.xlsx", {"q": "A1"}).content))
        hist = [[c.value for c in r] for r in wb["History"].iter_rows(min_row=2)]
        self.assertEqual([(h[1], h[2], h[15]) for h in hist], [("A1", "Magnet", "Add"), ("A1", "Holder", "Screen")])

    def test_download_can_be_uploaded_again(self):
        content = self.client.get("/material-master/download.xlsx").content
        r = self.client.post("/material-master/upload/", {"upload_type": "CHANGE",
                                                           "file": SimpleUploadedFile("d.xlsx", content)})
        batch = UploadBatch.objects.latest("id")
        self.assertEqual((batch.state, batch.summary["unchanged"]), (UploadBatch.State.PREVIEW, 2))


class ConcurrentUploadTests(TransactionTestCase):
    """H-5: 다른 사용자가 Upload 처리 중이면 거절."""

    def test_second_upload_is_rejected_while_first_is_running(self):
        admin = User.objects.create_user("admin1", "abcd1234", name="A", email="a@t.local",
                                         user_class=UserClass.ADMIN, id_status=IdStatus.APPROVED)
        self.client.force_login(admin)
        s = connection.settings_dict
        with psycopg.connect(host=s["HOST"], port=s["PORT"], user=s["USER"], password=s["PASSWORD"],
                             dbname=s["NAME"], autocommit=True) as other:
            other.execute("SELECT pg_advisory_lock(hashtext('upload:M1'))")  # 다른 사용자의 Upload 진행 중
            r = self.client.post("/material-master/upload/",
                                 {"upload_type": "ADD", "file": xlsx_file([row("A1", purchaser=None)])}, follow=True)
            self.assertContains(r, "Another user is uploading")
            other.execute("SELECT pg_advisory_unlock(hashtext('upload:M1'))")
        self.assertEqual(UploadBatch.objects.count(), 0)


class SafetyMoqTests(Base):
    """v1.1: 자재 안전재고·MOQ·Rounding Value (선택 열, 빈칸 = 0, 0 이상 정수)."""
    H = HEADERS + ["Mat. Safety Stock", "MOQ", "Rounding Value"]

    def test_upload_stores_values_and_blank_is_zero(self):
        self.upload_apply([row("A1") + [500, 1000, 250], row("B2") + [None, None, None]], headers=self.H)
        a, b = self.mat("A1"), self.mat("B2")
        self.assertEqual((a.safety_stock, a.moq, a.rounding_value), (500, 1000, 250))
        self.assertEqual((b.safety_stock, b.moq, b.rounding_value), (0, 0, 0))

    def test_negative_or_fraction_is_error(self):
        batch, _ = self.upload([row("A1") + [-1, 0, 0], row("B2") + [0, 1.5, 0], row("C3") + [0, 0, -5]],
                               headers=self.H)
        self.assertEqual((batch.state, batch.error_count), (UploadBatch.State.FAILED, 3))

    def test_screen_save_and_download_columns(self):
        self.upload_apply([row("A1")])
        m = self.mat("A1")
        data = {"sel": [m.pk], f"version_{m.pk}": m.version, f"unit_{m.pk}": "EA", f"lt_{m.pk}": 5,
                f"status_{m.pk}": m.status, f"ss_{m.pk}": "20", f"moq_{m.pk}": "300", f"rv_{m.pk}": "50"}
        self.client.post("/material-master/save/", data)
        m = self.mat("A1")
        self.assertEqual((m.safety_stock, m.moq, m.rounding_value), (20, 300, 50))
        wb = load_workbook(io.BytesIO(self.client.get("/material-master/download.xlsx").content))
        head = [c.value for c in next(wb.active.iter_rows(max_row=1))]
        self.assertIn("Mat. Safety Stock", head)
        self.assertIn("MOQ", head)
        self.assertIn("Rounding Value", head)
