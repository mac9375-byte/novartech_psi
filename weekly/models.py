"""Weekly Data (Module 5~8). 모든 행은 작업 주차(week, 'YYYY-Www')별로 저장하며 과거 주차는 보존한다 (Ⅳ-4)."""
from decimal import Decimal

from django.db import models

Q6 = {"max_digits": 20, "decimal_places": 6}


class InventoryRow(models.Model):
    """작업 주차 월요일 아침 재고, 합계만 (Ⅵ-5)."""

    class Category(models.TextChoices):
        ASSY = "ASSY", "Assy"
        MATERIAL = "MATERIAL", "Material"

    week = models.CharField(max_length=8, db_index=True)
    category = models.CharField(max_length=10, choices=Category.choices)
    code = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)
    qty = models.DecimalField(**Q6)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["week", "category", "code"], name="inv_unique")]


class PlanRow(models.Model):
    """RTF / Production Plan 14주 수량 (Ⅵ-6). qty = [W0..W+13] 정수 목록. auto = 자동 생성(0 채움) 행."""

    class Plan(models.TextChoices):
        RTF = "RTF", "RTF"
        PROD = "PROD", "Prod."

    week = models.CharField(max_length=8, db_index=True)
    plan = models.CharField(max_length=4, choices=Plan.choices)
    customer_code = models.CharField(max_length=100)
    qty = models.JSONField()
    auto = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["week", "plan", "customer_code"], name="plan_unique")]


class OpenPoRow(models.Model):
    """전체 PO Upload 원본 (Ⅵ-7). 계산값은 property."""

    week = models.CharField(max_length=8, db_index=True)
    seq = models.PositiveIntegerField()
    po_date = models.DateField()
    po_no = models.CharField(max_length=100)
    material_code = models.CharField(max_length=100, db_index=True)
    unit = models.CharField(max_length=10)
    po_qty = models.DecimalField(**Q6)
    currency = models.CharField(max_length=3, null=True, blank=True)
    unit_price = models.DecimalField(null=True, blank=True, **Q6)
    cancel = models.DecimalField(default=0, **Q6)
    gr = models.DecimalField(default=0, **Q6)
    in_transit = models.DecimalField(default=0, **Q6)
    vendor = models.CharField(max_length=200)

    class Meta:
        ordering = ["po_date", "po_no", "seq"]

    @property
    def final_po(self):
        return self.po_qty - self.cancel

    @property
    def remain(self):
        return self.final_po - self.gr - self.in_transit

    @property
    def open_qty(self):
        """Open PO = In Transit + Remain Q'ty (F-1)."""
        return self.in_transit + self.remain

    @property
    def amount(self):
        return None if self.unit_price is None else self.po_qty * self.unit_price

    @property
    def remain_amount(self):
        return None if self.unit_price is None else self.remain * self.unit_price


class SchedRow(models.Model):
    """사용자 입력 입고예정 (Manual Scheduled Receipt, Ⅵ-8). qty = [W0..W+13] 숫자 문자열 목록."""

    week = models.CharField(max_length=8, db_index=True)
    material_code = models.CharField(max_length=100)
    vendor = models.CharField(max_length=200)
    vendor_key = models.CharField(max_length=200)   # Material + Vendor 비교용 (앞뒤 공백 제거·대문자)
    unit = models.CharField(max_length=10)
    qty = models.JSONField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["week", "material_code", "vendor_key"], name="sched_unique")]

    @property
    def qty_dec(self):
        return [Decimal(x) for x in self.qty]
