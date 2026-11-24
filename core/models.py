from django.conf import settings
from django.db import models
from django.utils import timezone


class Status(models.TextChoices):
    """Master Data(Module 1~2) 상태."""
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"


class UploadBatch(models.Model):
    """Excel Upload 1회의 기록 (감사 기록 Ⅰ-9 + 미리보기 데이터)."""

    class State(models.TextChoices):
        PREVIEW = "PREVIEW", "Preview"      # 검증 완료, [반영] 대기
        APPLIED = "APPLIED", "Applied"
        CANCELLED = "CANCELLED", "Cancelled"
        FAILED = "FAILED", "Failed"         # Error가 있어 반영 불가

    module = models.CharField(max_length=10)                    # 예: M1
    upload_type = models.CharField(max_length=10, blank=True)   # ADD / CHANGE / INACTIVE
    source_filename = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=10, choices=State.choices)
    summary = models.JSONField(default=dict)        # 건수 + 변경 상세
    preview_rows = models.JSONField(default=list)   # 검증을 통과한 행 (정규화된 값)
    issues = models.JSONField(default=list)         # Error / Warning / Info 목록
    error_count = models.PositiveIntegerField(default=0)
    warning_count = models.PositiveIntegerField(default=0)
    applied_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]


class SystemStatus(models.Model):
    """재계산 필요 표시용 상태 (1행만 사용, Ⅳ-7-2)."""

    data_changed_at = models.DateTimeField(null=True, blank=True)
    last_calculated_at = models.DateTimeField(null=True, blank=True)
    last_calculated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name="+")

    @classmethod
    def get(cls):
        return cls.objects.get_or_create(pk=1)[0]

    @classmethod
    def mark_data_changed(cls):
        cls.objects.update_or_create(pk=1, defaults={"data_changed_at": timezone.now()})

    @property
    def need_recalculation(self):
        if not self.data_changed_at:
            return False
        return self.last_calculated_at is None or self.data_changed_at > self.last_calculated_at
