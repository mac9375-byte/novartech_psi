"""Class별 권한표 (Ⅴ-1-4). Backend 권한 검사는 반드시 이 표만 사용한다 (Ⅰ-9).

나중에 User에게 일부 Module 권한을 줄 때는 이 표만 바꾸면 된다 (Ⅴ-1-3).
업무 Module별 세분화(예: 'm1_upload')는 해당 Module 개발 시 추가한다.
"""
from functools import wraps

from django.core.exceptions import PermissionDenied

from .models import UserClass

PERMISSIONS = {
    UserClass.MASTER: {"user_manage"},
    UserClass.ADMIN: {"upload", "edit", "recalculate", "weekly_reset"},
    UserClass.USER: set(),
    UserClass.GUEST: set(),
}


def has_perm(user, action):
    return user.is_authenticated and action in PERMISSIONS.get(user.user_class, set())


def require(action):
    """View 데코레이터: 권한이 없으면 403 (URL·API 직접 호출 포함)."""

    def decorator(view):
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            if not has_perm(request.user, action):
                raise PermissionDenied
            return view(request, *args, **kwargs)

        return wrapped

    return decorator
