"""ISO 주차 계산 (Ⅳ-6). Current Week 판단은 베트남 Business Timezone 기준."""
import re
from datetime import date, timedelta
from zoneinfo import ZoneInfo

from django.utils import timezone

BUSINESS_TZ = ZoneInfo("Asia/Ho_Chi_Minh")
HORIZON = 14          # W0 ~ W+13 (Ⅲ-3)
PAST_WEEKS = 16       # 작업 주차 선택 범위: 지난 16주 (Ⅳ-6-2)
_WEEK_RE = re.compile(r"^(\d{4})-W(\d{2})$")


def week_of(d):
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def current_week(now=None):
    """베트남 시간 월요일 00:00에 바뀌는 ISO Current Week (예: '2026-W44')."""
    return week_of((now or timezone.now()).astimezone(BUSINESS_TZ).date())


def is_week(s):
    m = _WEEK_RE.match(s or "")
    if not m:
        return False
    try:
        date.fromisocalendar(int(m[1]), int(m[2]), 1)
    except ValueError:
        return False
    return True


def monday(week):
    return date.fromisocalendar(int(week[:4]), int(week[6:]), 1)


def add_weeks(week, n):
    """52주 다음을 1주로 고정하지 않고 ISO 달력으로 계산 (2026-W53 존재)."""
    return week_of(monday(week) + timedelta(weeks=n))


def horizon(week, n=HORIZON):
    return [add_weeks(week, i) for i in range(n)]


def rel(week, base):
    return (monday(week) - monday(base)).days // 7


def label(week, base):
    """화면 표기 'W44(W0)', 'W45(W+1)', 'W43(W-1)' (Ⅳ-6-1-2)."""
    d = rel(week, base)
    return f"W{week[6:]}(W{d:+d})" if d else f"W{week[6:]}(W0)"


def choices(cur=None):
    """작업 주차 Dropdown: Current Week ~ 지난 16주."""
    cur = cur or current_week()
    return [(w, label(w, cur)) for w in [add_weeks(cur, -i) for i in range(PAST_WEEKS + 1)]]


def selected(params, cur=None):
    """요청의 week 값이 선택 범위 안이면 그 주차, 아니면 Current Week."""
    cur = cur or current_week()
    w = params.get("week")
    return w if w in dict(choices(cur)) else cur
