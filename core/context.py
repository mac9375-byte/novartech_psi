from .models import SystemStatus
from .navigation import tabs


def permissions(request):
    """Template context processor: 화면 공통 버튼 표시용 권한 (서버 검사는 각 View의 @require가 따로 한다)."""
    from accounts.permissions import has_perm
    return {"can_recalculate": has_perm(request.user, "recalculate")}


def module_context(active, **extra):
    """업무 Module 화면 공통 값: 상단 탭, Final Calculation / Need Recalculation."""
    return {"tabs": tabs(active), "sys_status": SystemStatus.get(), **extra}
