"""테스트 공용 도우미."""
import io

from django.core.files.uploadedfile import SimpleUploadedFile
from openpyxl import Workbook

from accounts.models import IdStatus, User, UserClass


def xlsx(sheets, name="t.xlsx"):
    """{시트명: [Header 행, 데이터 행...]} → Upload 파일."""
    wb = Workbook()
    wb.remove(wb.active)
    for title, rows in sheets.items():
        ws = wb.create_sheet(title)
        for r in rows:
            ws.append(list(r))
    buf = io.BytesIO()
    wb.save(buf)
    return SimpleUploadedFile(name, buf.getvalue())


def user(username, cls=UserClass.ADMIN):
    return User.objects.create_user(username, "abcd1234", name=username, email=f"{username}@t.local",
                                    user_class=cls, id_status=IdStatus.APPROVED)


def material(code, unit="EA", lt=1, status="ACTIVE", desc=None):
    from materials.models import Material, UnitCode
    return Material.objects.create(material_code=code, unit=UnitCode.objects.get(code=unit), lead_time_weeks=lt,
                                   status=status, description=desc)


def assy(code, status="ACTIVE", assy_type="Magnet"):
    from assies.models import Assy
    return Assy.objects.create(customer_code=code, status=status, assy_type=assy_type)


def upload(client, prefix, sheets, upload_type="", apply=True):
    """Upload → (apply) → 최신 UploadBatch."""
    from core.models import UploadBatch
    client.post(f"{prefix}upload/", {"upload_type": upload_type, "file": xlsx(sheets)})
    batch = UploadBatch.objects.latest("id")
    if apply:
        client.post(f"{prefix}upload/{batch.pk}/apply/")
        batch.refresh_from_db()
    return batch
