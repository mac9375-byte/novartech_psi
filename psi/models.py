"""계산 결과 (계층 3, Ⅳ-7-0): Recalculate 실행 시에만 갱신. 주차별로 저장되어 과거 주차는 Snapshot으로 남는다."""
from fractions import Fraction

from django.db import models

Q10 = {"max_digits": 30, "decimal_places": 10}


class MrRow(models.Model):
    """Material Requirement 행 (Ⅵ-9). customer_code가 빈칸이면 Total 행. values = 14주 소요량(문자열 10자리)."""

    week = models.CharField(max_length=8, db_index=True)
    plan = models.CharField(max_length=4)                   # RTF / PROD
    material_code = models.CharField(max_length=100)
    customer_code = models.CharField(max_length=100, blank=True)
    qty_num = models.BigIntegerField(null=True)             # Assy 행의 BOM 소요원수 (같은 자재 여러 행은 합산)
    qty_den = models.BigIntegerField(null=True)
    values = models.JSONField()

    @property
    def qty(self):
        return Fraction(self.qty_num, self.qty_den) if self.qty_num is not None else None


class PsiRow(models.Model):
    """Material PSI 결과 (Ⅵ-10): Material × Plan."""

    week = models.CharField(max_length=8, db_index=True)
    plan = models.CharField(max_length=4)
    material_code = models.CharField(max_length=100)
    opening = models.DecimalField(**Q10)
    open_po = models.DecimalField(**Q10)
    req = models.JSONField()
    sr_manual = models.JSONField()
    sr_calc = models.JSONField()
    inv_balance = models.JSONField()
    po_balance = models.JSONField()
