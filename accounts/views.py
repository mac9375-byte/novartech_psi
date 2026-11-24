import secrets
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_not_required
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import LoginForm, MyInfoForm, SignupForm
from .models import IdStatus, User, UserClass
from .permissions import has_perm, require
from .validators import normalize_username, validate_username

MAX_FAILED_LOGINS = 5
LOCK_MINUTES = 10

MSG_LOCKED = "Too many failed attempts. Try again in 10 minutes. (Log-in 시도 횟수를 초과했습니다. 10분 후 다시 시도하세요.)"
MSG_INVALID = "Invalid Purchaser ID or Password."
MSG_STATUS = {
    IdStatus.REQUESTED: "Your ID is waiting for Master approval.",
    IdStatus.DISABLED: "This ID is disabled. Contact the Master.",
}

# Main 화면 메뉴 (PPT Main 01). url이 None이면 아직 개발 전 → 비활성 표시
MODULE_GROUPS = [
    ("Master DB", [("1. Material Master", None), ("2. Assy Master", None), ("3. BOM", None), ("4. Safety Stock", None)]),
    ("Weekly Data", [("5. Inventory", None), ("6. RTF/Production", None)]),
    ("PO", [("7. Open PO", None), ("8. Scheduled Receipt", None)]),
    ("Report", [("9. Material Requirement", None), ("10. Material PSI", None)]),
]


@login_not_required
def login_view(request):
    """Log-in (Ⅴ-2, Ⅴ-1-7)."""
    if request.user.is_authenticated:
        return redirect("main")
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = normalize_username(form.cleaned_data["username"])
        user = User.objects.filter(username=username).first()
        now = timezone.now()
        if user is None:
            form.add_error(None, MSG_INVALID)
        elif user.locked_until and user.locked_until > now:
            form.add_error(None, MSG_LOCKED)
        elif not user.check_password(form.cleaned_data["password"]):
            user.failed_login_count += 1
            if user.failed_login_count >= MAX_FAILED_LOGINS:
                user.failed_login_count = 0
                user.locked_until = now + timedelta(minutes=LOCK_MINUTES)
                form.add_error(None, MSG_LOCKED)
            else:
                form.add_error(None, MSG_INVALID)
            user.save(update_fields=["failed_login_count", "locked_until"])
        elif user.id_status != IdStatus.APPROVED:
            form.add_error(None, MSG_STATUS[user.id_status])
        else:
            user.failed_login_count = 0
            user.locked_until = None
            user.save(update_fields=["failed_login_count", "locked_until"])
            login(request, user)
            return redirect("me" if user.must_change_password else "main")
    return render(request, "accounts/login.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("login")


@login_not_required
def signup_view(request):
    """Sign up (Ⅴ-3): Class=User, ID Status=Requested로 저장."""
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        d = form.cleaned_data
        User.objects.create_user(
            d["username"], d["password"], name=d["name"], email=d["email"], tel=d["tel"],
            user_class=UserClass.USER, id_status=IdStatus.REQUESTED,
        )
        messages.success(request, "Sign up completed. You can log in after Master approval.")
        return redirect("login")
    return render(request, "accounts/signup.html", {"form": form})


@login_not_required
def check_id_view(request):
    """Sign up 'ID check' 버튼."""
    value = normalize_username(request.GET.get("id"))
    try:
        validate_username(value)
    except Exception as e:  # ValidationError
        return JsonResponse({"ok": False, "message": " ".join(e.messages)})
    if User.objects.filter(username=value).exists():
        return JsonResponse({"ok": False, "message": "This Purchaser ID is already in use."})
    return JsonResponse({"ok": True, "message": f"'{value}' is available."})


def main_view(request):
    """Main Navigation (Ⅴ-4)."""
    return render(request, "accounts/main.html", {
        "groups": MODULE_GROUPS,
        "can_manage_users": has_perm(request.user, "user_manage"),
    })


def me_view(request):
    """ID Info Pop-up (Ⅴ-4-2, Ⅴ-4-3): 모든 Class가 본인 정보 수정."""
    user = request.user
    initial = {"name": user.name, "email": user.email, "tel": user.tel}
    form = MyInfoForm(request.POST or None, user=user, initial=initial)
    if request.method == "POST" and form.is_valid():
        d = form.cleaned_data
        user.name, user.email, user.tel = d["name"], d["email"], d["tel"]
        if d.get("changing_password"):
            user.set_password(d["new_password"])
            user.must_change_password = False
        user.version = F("version") + 1
        user.save()
        user.refresh_from_db()
        update_session_auth_hash(request, user)
        messages.success(request, "Saved.")
        return redirect("main")
    return render(request, "accounts/me.html", {"form": form})


def _new_temp_password():
    # 규칙(영문+숫자, 8자 이상)을 항상 만족하도록 접두 'Tmp' + 숫자 보장
    return "Tmp" + secrets.token_urlsafe(9).replace("-", "x").replace("_", "y") + str(secrets.randbelow(10))


@require("user_manage")
def users_view(request):
    """User Management (Ⅴ-5): Master 전용."""
    if request.method == "POST":
        selected = [int(x) for x in request.POST.getlist("sel") if x.isdigit()]
        if not selected:
            messages.error(request, "Select rows first.")
        elif request.POST.get("action") == "save":
            _save_rows(request, selected)
        elif request.POST.get("action") == "reset":
            _reset_passwords(request, selected)
        return redirect("users")
    return render(request, "accounts/users.html", {
        "users": User.objects.all(),
        "class_choices": [c for c in UserClass.choices if c[0] != UserClass.MASTER],
        "status_choices": IdStatus.choices,
    })


def _save_rows(request, ids):
    valid_class = {UserClass.ADMIN, UserClass.USER, UserClass.GUEST}
    valid_status = set(IdStatus.values)
    saved = 0
    for pk in ids:
        if pk == request.user.pk:
            messages.error(request, "You cannot change your own Master account.")
            continue
        new_class = request.POST.get(f"class_{pk}")
        new_status = request.POST.get(f"status_{pk}")
        version = request.POST.get(f"version_{pk}", "")
        if new_class not in valid_class or new_status not in valid_status or not version.isdigit():
            messages.error(request, f"Invalid value (row id {pk}).")
            continue
        # Optimistic Lock: 조회 당시 version과 같을 때만 저장 (Ⅰ-11)
        updated = User.objects.filter(pk=pk, version=int(version)).exclude(user_class=UserClass.MASTER).update(
            user_class=new_class, id_status=new_status, version=F("version") + 1, updated_at=timezone.now(),
        )
        if updated:
            saved += 1
        else:
            messages.error(request, "Another user changed this data first. The latest data has been reloaded. "
                                    "(다른 사용자가 먼저 수정했습니다. 최신 Data를 다시 조회합니다.)")
    if saved:
        messages.success(request, f"{saved} row(s) saved.")


def _reset_passwords(request, ids):
    for user in User.objects.filter(pk__in=ids):
        if user.pk == request.user.pk:
            messages.error(request, "Change your own password in ID Info.")
            continue
        temp = _new_temp_password()
        with transaction.atomic():
            user.set_password(temp)
            user.must_change_password = True
            user.password_reset_at = timezone.now()
            user.failed_login_count = 0
            user.locked_until = None
            user.version = F("version") + 1
            user.save()
        send_mail(
            "[Material PSI] Temporary password",
            f"Hello {user.name},\n\nYour temporary password is: {temp}\n"
            "You must set a new password after logging in.",
            None, [user.email],
        )
        messages.success(request, f"Temporary password sent to {user.username} ({user.email}).")
