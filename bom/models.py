from fractions import Fraction

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone


class BomVersion(models.Model):
    """Assy 1개의 BOM 한 벌 (Ⅵ-3). is_current=True가 현재 BOM, 나머지는 History.

    Type·Model·Item은 등록 시점 Assy Master 값을 함께 저장해 History에 '이력 시점 값'으로 쓴다 (F-8).
    """

    customer_code = models.CharField(max_length=100, db_index=True)
    is_current = models.BooleanField(default=True)
    updated_at = models.DateTimeField(default=timezone.now)   # 같은 Assy의 모든 행이 같은 Update (F-7)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    upload_batch = models.ForeignKey("core.UploadBatch", null=True, blank=True, on_delete=models.PROTECT,
                                     related_name="+")
    assy_type = models.TextField(null=True, blank=True)
    model_name = models.TextField(null=True, blank=True)
    item = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["customer_code", "updated_at", "id"]
        constraints = [models.UniqueConstraint(fields=["customer_code"], condition=Q(is_current=True),
                                               name="bom_one_current_per_assy")]


class BomLine(models.Model):
    """BOM 자재 행. 같은 Assy 안 같은 Material 여러 행 허용, 병합하지 않음 (Ⅵ-3-5)."""

    version = models.ForeignKey(BomVersion, on_delete=models.CASCADE, related_name="lines")
    seq = models.PositiveIntegerField()                       # 업로드 순서 (BOM Line ID 순)
    material_code = models.CharField(max_length=100, db_index=True)
    unit = models.CharField(max_length=10)
    qty_num = models.BigIntegerField()                        # 소요원수 = qty_num / qty_den (분수 저장, Q-1)
    qty_den = models.BigIntegerField()
    desc_snap = models.TextField(null=True, blank=True)       # 등록 시점 Material Master 값 (History용)
    spec_snap = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["version", "seq"]

    @property
    def qty(self):
        return Fraction(self.qty_num, self.qty_den)
