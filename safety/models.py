from django.conf import settings
from django.db import models
from django.utils import timezone


class SafetyStock(models.Model):
    """Assy(Customer Code)별 안전재고 (Ⅵ-4). Assy 기준정보는 Assy Master에서 조회 (저장 안 함)."""

    customer_code = models.CharField(max_length=100, unique=True)
    qty = models.PositiveIntegerField()
    updated_at = models.DateTimeField(default=timezone.now)   # 실제로 바뀐 Upload 시각
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")

    class Meta:
        ordering = ["customer_code"]


class SafetyHistory(models.Model):
    """Safety Q'ty 변경 이력 (추가 / 변경 / 삭제, Ⅵ-4-11)."""

    customer_code = models.CharField(max_length=100, db_index=True)
    qty = models.PositiveIntegerField(null=True)               # 삭제 행은 삭제 전 값
    change_type = models.CharField(max_length=10)              # Add / Change / Delete
    changed_at = models.DateTimeField()
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    upload_batch = models.ForeignKey("core.UploadBatch", null=True, on_delete=models.PROTECT, related_name="+")

    class Meta:
        ordering = ["customer_code", "changed_at", "id"]
