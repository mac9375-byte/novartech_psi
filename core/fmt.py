"""화면 숫자 표시."""
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction


def num(v, places=6):
    """천 단위 쉼표, 소수는 places 자리까지(끝 0 제거). None은 빈칸."""
    if v is None or v == "":
        return ""
    d = Decimal(str(v)) if not isinstance(v, Decimal) else v
    q = d.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
    s = f"{q:,.{places}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def frac(f):
    """소요원수 표시: 정수는 그대로, 아니면 분수 '1/1,000' (Ⅵ-3-9)."""
    if f is None:
        return ""
    f = Fraction(f)
    if f.denominator == 1:
        return f"{f.numerator:,}"
    if f.denominator > 10 ** 6:
        return num(Decimal(f.numerator) / Decimal(f.denominator), 10)
    return f"{f.numerator:,}/{f.denominator:,}"
