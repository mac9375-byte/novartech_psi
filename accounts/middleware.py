import zoneinfo

from django.shortcuts import redirect
from django.utils import timezone

ALLOWED_WHILE_TEMP_PASSWORD = ("/me/", "/logout/", "/static/")
POC_USER = "poc_admin"


class PocAutoLoginMiddleware:
    """PoC 점검용: 로그인 없이 Admin(poc_admin)으로 자동 로그인.

    DEBUG(개발 모드)이고 settings.POC_SKIP_LOGIN이 켜져 있을 때만 동작한다. 운영 배포(DEBUG 끔) 시 자동으로 꺼진다.
    ponytail: PoC 편의 기능, 운영 전환 시 이 Middleware와 설정을 삭제
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.conf import settings
        if (settings.DEBUG and getattr(settings, "POC_SKIP_LOGIN", False) and not request.user.is_authenticated
                and not request.path.startswith(("/login/", "/signup/", "/logout/", "/static/"))):
            # Log-in 화면에서는 직접 로그인 가능 (다른 계정으로 점검할 때)
            from django.contrib.auth import login
            from .models import IdStatus, User, UserClass
            user, created = User.objects.get_or_create(username=POC_USER, defaults={
                "name": "PoC Admin", "email": "poc_admin@novatech.local",
                "user_class": UserClass.ADMIN, "id_status": IdStatus.APPROVED})
            if created:
                user.set_unusable_password()
                user.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return self.get_response(request)


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
