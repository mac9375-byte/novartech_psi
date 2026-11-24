import zoneinfo

from django.shortcuts import redirect
from django.utils import timezone

ALLOWED_WHILE_TEMP_PASSWORD = ("/me/", "/logout/", "/static/")


class ForcePasswordChangeMiddleware:
    """임시 P/W 사용자는 새 P/W 저장 전까지 ID Info 외 화면 사용 불가 (Ⅴ-1-6, Ⅴ-4-3)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if (
            user.is_authenticated
            and user.must_change_password
            and not request.path.startswith(ALLOWED_WHILE_TEMP_PASSWORD)
        ):
            return redirect("me")
        return self.get_response(request)


class UserTimezoneMiddleware:
    """화면 시간 표시: 브라우저가 알려준 Timezone(쿠키 'tz') 사용. 없으면 settings.TIME_ZONE (Ⅳ-6-4)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            timezone.activate(zoneinfo.ZoneInfo(request.COOKIES.get("tz", "")))
        except (zoneinfo.ZoneInfoNotFoundError, ValueError):
            timezone.deactivate()
        return self.get_response(request)
