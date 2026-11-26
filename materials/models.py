from django.conf import settings
from django.db import models
from django.utils import timezone

from core.models import Status  # Master Data 공통 상태 (Active / Inactive)


class UnitCode(models.Model):
    """Unit 허용값. 값 추가는 이 표에 행만 추가 (코드 수정 불필요, Ⅵ-1-4 ④)."""

    code = models.CharField(max_length=10, primary_key=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "code"]

    def __str__(self):
        return self.code




class Material(models.Model):
    """Material Master 현재값 (Ⅵ-1). Key = material_code (대문자 정규화)."""

    material_code = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    spec = models.TextField(null=True, blank=True)
    unit = models.ForeignKey(UnitCode, on_delete=models.PROTECT, related_name="+")
    purchaser = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                  on_delete=models.PROTECT, related_name="+")
    vendor = models.TextField(null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    lead_time_weeks = models.PositiveSmallIntegerField()
    safety_stock = models.PositiveIntegerField(default=0)   # v1.1 자재 안전재고 (Assy Safety Stock과 별개)
    moq = models.PositiveIntegerField(default=0)            # v1.1 최소발주수량, 0 = 미적용
    rounding_value = models.PositiveIntegerField(default=0) # v1.1 발주 단위(포장 단위) 배수, 0 = 미적용
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, related_name="+")
    # 'Update' 열: 값이 실제로 바뀐 경우에만 갱신하므로 auto_now를 쓰지 않는다
    updated_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, related_name="+")
    inactive_at = models.DateTimeField(null=True, blank=True)
    inactive_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                    on_delete=models.PROTECT, related_name="+")
    version = models.PositiveIntegerField(default=1)  # Optimistic Lock (Ⅰ-11)

    class Meta:
        ordering = ["material_code"]

    def __str__(self):
        return self.material_code


class MaterialHistory(models.Model):
    """변경 이력: 행이 생기거나 바뀔 때마다 바뀐 뒤 값을 그대로 복사 (F-8 이력 시점 값)."""

    class ChangeType(models.TextChoices):
        ADD = "Add"
        CHANGE = "Change"
        INACTIVE = "Inactive"
        REACTIVATE = "Reactivate"
        SCREEN = "Screen"

    material_code = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=True, blank=True)
    spec = models.TextField(null=True, blank=True)
    unit = models.CharField(max_length=10)
    purchaser_id_text = models.CharField(max_length=150, null=True, blank=True)
    purchaser_name = models.CharField(max_length=100, null=True, blank=True)
    vendor = models.TextField(null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    lead_time_weeks = models.PositiveSmallIntegerField()
    safety_stock = models.PositiveIntegerField(default=0)
    moq = models.PositiveIntegerField(default=0)
    rounding_value = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10)
    change_type = models.CharField(max_length=10, choices=ChangeType.choices)
    changed_at = models.DateTimeField()
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    upload_batch = models.ForeignKey("core.UploadBatch", null=True, blank=True, on_delete=models.PROTECT,
                                     related_name="+")

    class Meta:
        ordering = ["material_code", "changed_at", "id"]

    @classmethod
    def record(cls, m, change_type, user, when, batch=None):
        cls.objects.create(
            material_code=m.material_code, description=m.description, spec=m.spec, unit=m.unit_id,
            purchaser_id_text=m.purchaser.username if m.purchaser else None,
            purchaser_name=m.purchaser.name if m.purchaser else None,
            vendor=m.vendor, country=m.country, lead_time_weeks=m.lead_time_weeks,
            safety_stock=m.safety_stock, moq=m.moq,
            rounding_value=m.rounding_value, status=m.status,
            change_type=change_type, changed_at=when, changed_by=user, upload_batch=batch,
        )
