"""Recalculate (Ⅳ-7-1) — Module 1~8 현재 값으로 Module 9·10을 Current Week에 대해 다시 계산한다.

계산 단계를 나눠 두어 다음 버전에서 발주필요수량 단계를 추가할 수 있게 한다 (Ⅰ-5 (b)).
  1) check_errors      : Error가 있으면 계산 중단 (값을 임의로 보정하지 않음)
  2) requirements      : Σ(Assy 주별 계획 × BOM 소요원수), RTF 14주차는 + Safety Stock
  3) supply            : 기초재고, 입고예정(Manual + Calculated), Open PO
  4) balances          : 재고 과부족, PO 과부족
  5) save              : 해당 주차 결과 교체 저장
"""
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction

from django.db import connection, transaction
from django.utils import timezone

from core import lookup, weeks
from core.models import OperationLog, SystemStatus

from .models import MrRow, PsiRow

N = weeks.HORIZON
PLACES = Decimal("1e-10")      # 내부 계산값 소수점 10자리 (M9-1)


class RecalcBusy(Exception):
    pass


def dec(f):
    """Fraction → Decimal(10자리)."""
    with localcontext() as ctx:
        ctx.prec = 40
        return (Decimal(f.numerator) / Decimal(f.denominator)).quantize(PLACES)


def _cum(xs):
    out, s = [], Fraction(0)
    for x in xs:
        s += x
        out.append(s)
    return out


def check_errors(week):
    """BOM Unit ≠ Material Master Unit (F-14), 입고예정 > Open PO (Ⅶ-10) → Error."""
    from bom.models import BomLine
    from weekly.services import scheduled_receipts
    errors = []
    mats = lookup.materials()
    for l in BomLine.objects.filter(version__is_current=True).select_related("version"):
        m = mats.get(l.material_code)
        if m and l.unit != m.unit_id:
            errors.append(f"BOM {l.version.customer_code} / {l.material_code}: Unit '{l.unit}' ≠ Material Master "
                          f"Unit '{m.unit_id}'. Re-upload the BOM (Change).")
    sr = scheduled_receipts(week)
    for it in sr.values():
        if it["diff"] < 0:
            errors.append(f"Scheduled Receipt > Open PO: {it['mat']} / {it['vendor']} (difference {it['diff']:,}).")
    return errors, sr


def requirements(week, warnings):
    """{plan: {material: {'total': [14], 'assy': {cust: (소요원수, [14])}}}}, BOM 미등록 Assy 수."""
    from bom.services import bom_map
    from safety.services import safety_map
    from weekly.models import PlanRow
    bom, safety = bom_map(), safety_map()
    plans = list(PlanRow.objects.filter(week=week))
    assies = lookup.assies()
    res = {"RTF": defaultdict(lambda: {"total": [Fraction(0)] * N, "assy": {}}),
           "PROD": defaultdict(lambda: {"total": [Fraction(0)] * N, "assy": {}})}
    no_bom = set()
    for p in plans:
        q = [Fraction(x) for x in p.qty]
        if p.plan == "RTF":
            q[-1] += safety.get(p.customer_code, 0)        # Safety는 RTF 14주차에만 (C-2)
        a = assies.get(p.customer_code)
        if any(q) and not a:
            warnings.append(f"Assy {p.customer_code} ({p.plan}): not in Assy Master (No DB); included.")
        elif any(q) and a.status == "INACTIVE":
            warnings.append(f"Assy {p.customer_code} ({p.plan}): Inactive; included.")
        b = bom.get(p.customer_code)
        if not b:
            if any(q):
                no_bom.add(p.customer_code)                # 소요량 0 간주 (Ⅲ-4-3)
            continue
        for mat, per in b.items():
            vals = [x * per for x in q]
            node = res[p.plan][mat]
            node["assy"][p.customer_code] = (per, vals)
            node["total"] = [t + v for t, v in zip(node["total"], vals)]
    for code in sorted(no_bom):
        warnings.append(f"Assy {code}: No BOM — requirement counted as 0 (BOM 미등록).")
    return res, bom, len(no_bom)


def supply(week, bom, sr, warnings):
    from weekly.models import InventoryRow
    mat_inv, assy_inv = defaultdict(Fraction), defaultdict(Fraction)
    for r in InventoryRow.objects.filter(week=week):
        (mat_inv if r.category == "MATERIAL" else assy_inv)[r.code] += Fraction(r.qty)
    rtf_open = defaultdict(Fraction, mat_inv)
    for cust, qty in assy_inv.items():                      # Assy 재고 → Material 환산 (C-1, RTF 기준만)
        for mat, per in bom.get(cust, {}).items():
            rtf_open[mat] += qty * per
    manual = defaultdict(lambda: [Fraction(0)] * N)
    calc = defaultdict(lambda: [Fraction(0)] * N)
    open_po = defaultdict(Fraction)
    for it in sr.values():
        manual[it["mat"]] = [a + Fraction(b) for a, b in zip(manual[it["mat"]], it["manual"])]
        calc[it["mat"]] = [a + Fraction(b) for a, b in zip(calc[it["mat"]], it["calc"])]
        open_po[it["mat"]] += Fraction(it["in_transit"] + it["remain"])
        if it["skipped"]:
            warnings.append(f"Material {it['mat']} / {it['vendor']}: not in Material Master (No DB); "
                            "calculated receipt skipped.")
    return {"RTF": rtf_open, "PROD": defaultdict(Fraction, mat_inv)}, manual, calc, open_po


def recalculate(week, user):
    """성공하면 OperationLog, 실패(Error)면 기존 결과 유지 + 실패 기록."""
    from safety.services import safety_map
    from weekly.services import regenerate_auto_plans
    with transaction.atomic():
        with connection.cursor() as cur:
            cur.execute("SELECT pg_try_advisory_xact_lock(hashtext('recalculate'))")
            if not cur.fetchone()[0]:
                raise RecalcBusy("Another user is recalculating. The result will be shown when it finishes. "
                                 "(다른 사용자가 재계산 중입니다.)")
        errors, sr = check_errors(week)
        if errors:
            return OperationLog.objects.create(kind=OperationLog.Kind.RECALC, week=week, user=user, success=False,
                                               error_count=len(errors), details={"errors": errors[:200]})
        warnings = []
        auto = regenerate_auto_plans(week, safety_map().keys())   # 규칙 B: Safety에만 있는 Code
        res, bom, no_bom = requirements(week, warnings)
        opening, manual, calc, open_po = supply(week, bom, sr, warnings)
        mats = lookup.materials()
        used = set(res["RTF"]) | set(res["PROD"]) | set(opening["RTF"]) | set(manual) | set(open_po)
        for m in sorted(used):
            if m not in mats:
                warnings.append(f"Material {m}: not in Material Master (No DB); included.")
            elif mats[m].status == "INACTIVE":
                warnings.append(f"Material {m}: Inactive; included.")

        MrRow.objects.filter(week=week).delete()
        PsiRow.objects.filter(week=week).delete()
        mr, psi = [], []
        zero = [Fraction(0)] * N
        for plan in ("RTF", "PROD"):
            for mat, node in res[plan].items():
                mr.append(MrRow(week=week, plan=plan, material_code=mat, values=[str(dec(v)) for v in node["total"]]))
                mr += [MrRow(week=week, plan=plan, material_code=mat, customer_code=c, qty_num=per.numerator,
                             qty_den=per.denominator, values=[str(dec(v)) for v in vals])
                       for c, (per, vals) in node["assy"].items()]
            for mat in sorted(used):
                req = res[plan][mat]["total"] if mat in res[plan] else zero
                sr_total = [a + b for a, b in zip(manual.get(mat, zero), calc.get(mat, zero))]
                op, po = opening[plan].get(mat, Fraction(0)), open_po.get(mat, Fraction(0))
                inv = [op + s - r for s, r in zip(_cum(sr_total), _cum(req))]       # 재고 과부족
                po_bal = [op + po - r for r in _cum(req)]                          # PO 과부족 (입고예정 미포함)
                psi.append(PsiRow(week=week, plan=plan, material_code=mat, opening=dec(op), open_po=dec(po),
                                  req=[str(dec(v)) for v in req],
                                  sr_manual=[str(dec(v)) for v in manual.get(mat, zero)],
                                  sr_calc=[str(dec(v)) for v in calc.get(mat, zero)],
                                  inv_balance=[str(dec(v)) for v in inv], po_balance=[str(dec(v)) for v in po_bal]))
        MrRow.objects.bulk_create(mr)
        PsiRow.objects.bulk_create(psi)
        now = timezone.now()
        SystemStatus.objects.update_or_create(pk=1, defaults={"last_calculated_at": now, "last_calculated_by": user})
        return OperationLog.objects.create(
            kind=OperationLog.Kind.RECALC, week=week, user=user, at=now, success=True, warning_count=len(warnings),
            details={"warnings": warnings[:300], "no_bom": no_bom, "auto_generated": auto, "materials": len(used),
                     "modules": "Material Requirement, Material PSI"})


def weekly_reset(week, user):
    """작업 주차의 Module 5~8 데이터만 삭제 (Ⅳ-7-4). Module 1~4와 과거 주차, 계산 결과는 유지."""
    from weekly.models import InventoryRow, OpenPoRow, PlanRow, SchedRow
    with transaction.atomic():
        counts = {m.__name__: m.objects.filter(week=week).delete()[0]
                  for m in (InventoryRow, PlanRow, OpenPoRow, SchedRow)}
        SystemStatus.mark_data_changed()
        return OperationLog.objects.create(kind=OperationLog.Kind.RESET, week=week, user=user, details=counts)
