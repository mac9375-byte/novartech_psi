from .models import SystemStatus
from .navigation import tabs


def module_context(active, **extra):
    """업무 Module 화면 공통 값: 상단 탭, Final Calculation / Need Recalculation."""
    return {"tabs": tabs(active), "sys_status": SystemStatus.get(), **extra}
