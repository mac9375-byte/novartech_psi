from django.conf import settings
from django.db import models
from django.utils import timezone

from core.models import Status


class Assy(models.Model):
    """Assy Master 현재값 (Ⅵ-2). Key = customer_code (대문자 정규화). Assy Unit은 EA 고정이라 저장하지 않음."""

    customer_code = models.CharField(max_length=100, unique=True)
    assy_code = models.CharField(max_length=100, null=True, blank=True, db_index=True)  # Key 아님, 중복 허용
    assy_type = models.TextField(null=True, blank=True)    # 화면 'Type'
    model_name = models.TextField(null=True, blank=True)   # 화면 'Model'
    item = models.TextField(null=True, blank=True)
    customer = models.TextField(null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, related_name="+")
    updated_at = models.DateTimeField(default=timezone.now)  # 값이 실제로 바뀐 경우에만 갱신
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, related_name="+")
    inactive_at = models.DateTimeField(null=True, blank=True)
    inactive_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                    on_delete=models.PROTECT, related_name="+")
    version = models.PositiveIntegerField(default=1)  # Optimistic Lock (Ⅰ-11)

    class Meta:
        ordering = ["customer_code"]

    def __str__(self):
        return self.customer_code


class AssyHistory(models.Model):
    """변경 이력: 바뀐 뒤 값을 그대로 복사 (F-8 이력 시점 값)."""

    customer_code = models.CharField(max_length=100, db_index=True)
    assy_code = models.CharField(max_length=100, null=True, blank=True)
    assy_type = models.TextField(null=True, blank=True)
    model_name = models.TextField(null=True, blank=True)
    item = models.TextField(null=True, blank=True)
    customer = models.TextField(null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10)
    change_type = models.CharField(max_length=10)  # Add / Change / Inactive / Reactivate / Screen
    changed_at = models.DateTimeField()
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    upload_batch = models.ForeignKey("core.UploadBatch", null=True, blank=True, on_delete=models.PROTECT,
                                     related_name="+")

    class Meta:
        ordering = ["customer_code", "changed_at", "id"]

    @classmethod
    def record(cls, a, change_type, user, when, batch=None):
        cls.objects.create(
            customer_code=a.customer_code, assy_code=a.assy_code, assy_type=a.assy_type, model_name=a.model_name,
            item=a.item, customer=a.customer, country=a.country, status=a.status,
            change_type=change_type, changed_at=when, changed_by=user, upload_batch=batch,
        )
