"""Assy Master 테스트 (Ⅵ-2 Acceptance Criteria, 설계/04)."""
import io

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from openpyxl import Workbook, load_workbook

from accounts.models import IdStatus, User, UserClass
from core.models import Status, UploadBatch
from materials.models import Material, UnitCode

from .models import Assy, AssyHistory

HEADERS = ["Customer Code", "Assy Code", "Type", "Model", "Item", "Customer", "Country"]


def xlsx_file(rows, headers=HEADERS, sheet="MD_Assy"):
    wb = Workbook()
    ws = wb.active
    ws.title = sheet
    ws.append(headers)
    for r in rows:
        ws.append(r)
    buf = io.BytesIO()
    wb.save(buf)
    return SimpleUploadedFile("a.xlsx", buf.getvalue())


def row(cust, assy="MGMZ18001", typ="Magnet", model="Z FLIP6", item="B6 MAIN L", customer="SEVT", country="Vina"):
    return [cust, assy, typ, model, item, customer, country]


class AssyTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user("admin1", "abcd1234", name="Admin", email="a@t.local",
                                              user_class=UserClass.ADMIN, id_status=IdStatus.APPROVED)
        self.client.force_login(self.admin)

    def upload(self, rows, upload_type="CHANGE", **kw):
        self.client.post("/assy-master/upload/", {"upload_type": upload_type, "file": xlsx_file(rows, **kw)})
        return UploadBatch.objects.latest("id")

    def upload_apply(self, rows, upload_type="CHANGE", **kw):
        batch = self.upload(rows, upload_type, **kw)
        self.client.post(f"/assy-master/upload/{batch.pk}/apply/")
        batch.refresh_from_db()
        return batch

    def assy(self, code):
        return Assy.objects.get(customer_code=code)

    def test_only_customer_code_is_required_and_codes_normalized(self):
        batch = self.upload_apply([[" gh61-16650a ", "mgmz21022"]], headers=["Customer Code", "Assy Code"])
        self.assertEqual(batch.state, UploadBatch.State.APPLIED)
        a = self.assy("GH61-16650A")
        self.assertEqual((a.assy_code, a.assy_type, a.status), ("MGMZ21022", None, Status.ACTIVE))

    def test_customer_code_unique_but_assy_code_duplicates_allowed(self):
        self.upload_apply([row("A1", assy="X1"), row("A2", assy="X1")])
        self.assertEqual(Assy.objects.filter(assy_code="X1").count(), 2)
        batch = self.upload([row("B1"), row("b1")])
        self.assertEqual(batch.state, UploadBatch.State.FAILED)
        self.assertIn("Duplicate Customer Code", batch.issues[0]["reason"])

    def test_assy_code_may_equal_a_material_code(self):
        unit = UnitCode.objects.get(code="EA")
        Material.objects.create(material_code="MGMZ21022", unit=unit, lead_time_weeks=1)
        self.upload_apply([row("4605000219", assy="MGMZ21022")])
        self.assertTrue(Assy.objects.filter(customer_code="4605000219", assy_code="MGMZ21022").exists())

    def test_numeric_customer_code_and_exponent_error(self):
        self.upload_apply([row(4605000219)])
        self.assertTrue(Assy.objects.filter(customer_code="4605000219").exists())
        batch = self.upload([row("3.04E+11")])
        self.assertIn("Exponent", batch.issues[0]["reason"])

    def test_add_change_inactive_flow(self):
        self.upload_apply([row("A1"), row("A2")], "ADD")
        b = self.upload_apply([row("A1", typ="Halbah"), row("A3")], "ADD")
        self.assertEqual((b.summary["new"], b.summary["skipped"]), (1, 1))
        self.assertEqual(self.assy("A1").assy_type, "Magnet")
        b = self.upload_apply([row("A1", typ="Halbah", model=None)])
        self.assertEqual(b.summary["changed"], 1)
        self.assertEqual((self.assy("A1").assy_type, self.assy("A1").model_name), ("Halbah", None))
        b = self.upload_apply([["A2"], ["NONE"]], "INACTIVE", headers=["Customer Code"])
        self.assertEqual((b.summary["inactive"], b.summary["skipped"]), (1, 1))
        self.assertEqual(self.assy("A2").status, Status.INACTIVE)
        b = self.upload_apply([row("A2")])
        self.assertEqual(b.summary["reactivated"], 1)
        self.assertEqual(list(AssyHistory.objects.filter(customer_code="A2").values_list("change_type", flat=True)),
                         ["Add", "Inactive", "Reactivate"])

    def test_header_type_is_case_sensitive(self):
        batch = self.upload([row("A1")], headers=["Customer Code", "Assy Code", "TYPE", "Model", "Item",
                                                  "Customer", "Country"])
        self.assertIn(("Info", "TYPE"), [(i["level"], i["field"]) for i in batch.issues])  # 'TYPE'은 정의 안 된 열

    def test_screen_edit_status_filter_and_lock(self):
        self.upload_apply([row("A1")])
        a = self.assy("A1")
        data = {"sel": [a.pk], f"version_{a.pk}": a.version, f"assy_{a.pk}": "mgmz99", f"type_{a.pk}": "MPS",
                f"model_{a.pk}": "", f"item_{a.pk}": "", f"customer_{a.pk}": "SEV", f"country_{a.pk}": "Vina",
                f"status_{a.pk}": "INACTIVE"}
        self.client.post("/assy-master/save/", data)
        a.refresh_from_db()
        self.assertEqual((a.assy_code, a.assy_type, a.model_name, a.status, a.version),
                         ("MGMZ99", "MPS", None, Status.INACTIVE, 2))
        self.assertNotContains(self.client.get("/assy-master/"), ">A1<")
        self.assertContains(self.client.get("/assy-master/", {"status": "INACTIVE", "field": "type", "q": "mp"}), ">A1<")
        r = self.client.post("/assy-master/save/", data, follow=True)  # 이전 version으로 다시 저장
        self.assertContains(r, "Another user changed this data first")

    def test_download_reupload_and_history(self):
        self.upload_apply([row("A1"), row("A2", customer="SEVT")])
        content = self.client.get("/assy-master/download.xlsx", {"status": "ALL"}).content
        ws = load_workbook(io.BytesIO(content))["MD_Assy"]
        self.assertEqual([c.value for c in ws[1]], ["No", "Customer Code", "Assy Code", "Type", "Model", "Item",
                                                    "Customer", "Country", "Update", "Status"])
        self.client.post("/assy-master/upload/", {"upload_type": "CHANGE", "file": SimpleUploadedFile("d.xlsx", content)})
        self.assertEqual(UploadBatch.objects.latest("id").summary["unchanged"], 2)
        hist = load_workbook(io.BytesIO(self.client.get("/assy-master/history.xlsx", {"q": "A1"}).content))["History"]
        self.assertEqual([c.value for c in hist[2]][1], "A1")
        self.assertEqual([c.value for c in hist[2]][10], "Add")

    def test_non_admin_view_only(self):
        self.upload_apply([row("A1")])
        a = self.assy("A1")
        for cls in [UserClass.MASTER, UserClass.USER, UserClass.GUEST]:
            u = User.objects.create_user(f"u{cls.lower()}", "abcd1234", name="x", email="x@t.local",
                                         user_class=cls, id_status=IdStatus.APPROVED)
            self.client.force_login(u)
            self.assertEqual(self.client.post("/assy-master/save/", {"sel": [a.pk]}).status_code, 403)
            self.assertEqual(self.client.post("/assy-master/upload/", {"upload_type": "ADD"}).status_code, 403)
            page = self.client.get("/assy-master/")
            self.assertContains(page, ">A1<")
            self.assertNotContains(page, 'name="type_')
        self.assertEqual(self.client.get("/assy-master/download.xlsx").status_code, 200)

    def test_main_menu_enables_assy_master(self):
        self.assertContains(self.client.get("/"), 'href="/assy-master/"')
