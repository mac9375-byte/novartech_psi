"""공통 기반 기능 테스트 (설계/01 A-14, 설계/02 7절)."""
from datetime import timedelta
from io import StringIO

from django.conf import settings
from django.core import mail
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from .models import IdStatus, User, UserClass

PW = "abcd1234"


def make_user(username, user_class=UserClass.USER, status=IdStatus.APPROVED, **kw):
    return User.objects.create_user(username, PW, name=username, email=f"{username}@test.local",
                                    user_class=user_class, id_status=status, **kw)


class SignupLoginTests(TestCase):
    def signup(self, username="Nana.Kang", password=PW, password2=None):
        return self.client.post("/signup/", {
            "username": username, "password": password, "password2": password2 or password,
            "name": "Nana", "email": "nana@test.local", "tel": "+84-1",
        })

    def test_1_signup_creates_requested_user_and_login_is_blocked(self):
        self.signup()
        u = User.objects.get()
        self.assertEqual((u.username, u.user_class, u.id_status), ("nana.kang", UserClass.USER, IdStatus.REQUESTED))
        r = self.client.post("/login/", {"username": "nana.kang", "password": PW})
        self.assertContains(r, "waiting for Master approval")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_2_approved_user_can_log_in(self):
        make_user("nova007")
        r = self.client.post("/login/", {"username": "NOVA007", "password": PW})
        self.assertRedirects(r, "/")

    def test_3_five_failures_lock_for_10_minutes_then_success_resets(self):
        u = make_user("nova007")
        for _ in range(5):
            r = self.client.post("/login/", {"username": "nova007", "password": "wrong999"})
        self.assertContains(r, "Try again in 10 minutes")
        r = self.client.post("/login/", {"username": "nova007", "password": PW})
        self.assertContains(r, "Try again in 10 minutes")  # 맞는 P/W도 잠금 중 거부
        User.objects.filter(pk=u.pk).update(locked_until=timezone.now() - timedelta(seconds=1))
        self.client.post("/login/", {"username": "nova007", "password": "wrong999"})
        r = self.client.post("/login/", {"username": "nova007", "password": PW})
        self.assertRedirects(r, "/")
        u.refresh_from_db()
        self.assertEqual(u.failed_login_count, 0)

    def test_6_disabled_user_cannot_log_in(self):
        make_user("tomas", status=IdStatus.DISABLED)
        r = self.client.post("/login/", {"username": "tomas", "password": PW})
        self.assertContains(r, "disabled")

    def test_7_session_expires_after_2_hours_idle(self):
        self.assertEqual(settings.SESSION_COOKIE_AGE, 7200)
        self.assertTrue(settings.SESSION_SAVE_EVERY_REQUEST)

    def test_8_password_is_hashed(self):
        u = make_user("nova007")
        self.assertNotIn(PW, u.password)
        self.assertTrue(u.password.startswith("pbkdf2_"))

    def test_username_rules(self):
        for bad in ["a b", "kim@nova", "", "한글"]:
            self.signup(username=bad)
        self.assertEqual(User.objects.count(), 0)
        for good in ["jet.son", "hong_12", "a-b"]:
            self.signup(username=good)
        self.assertEqual(User.objects.count(), 3)
        self.signup(username="JET.SON")  # 대소문자 무시 중복
        self.assertEqual(User.objects.count(), 3)

    def test_password_rules(self):
        for bad in ["abcdefgh", "12345678", "abc1234", "abcd 1234"]:
            self.signup(username="x1", password=bad)
        self.signup(username="x1", password=PW, password2="abcd9999")
        self.assertEqual(User.objects.count(), 0)
        self.signup(username="x1", password="abcd123!")  # 특수문자 허용
        self.assertEqual(User.objects.count(), 1)

    def test_check_id_endpoint(self):
        make_user("nova007")
        self.assertFalse(self.client.get("/signup/check-id/", {"id": "Nova007"}).json()["ok"])
        self.assertTrue(self.client.get("/signup/check-id/", {"id": "nova008"}).json()["ok"])

    def test_pages_require_login(self):
        for url in ["/", "/me/", "/users/"]:
            self.assertRedirects(self.client.get(url), f"/login/?next={url}")


class UserManagementTests(TestCase):
    def setUp(self):
        self.master = make_user("novamaster", UserClass.MASTER)
        self.target = make_user("abydon", status=IdStatus.REQUESTED)

    def test_5_only_master_can_access_user_management(self):
        for cls in [UserClass.ADMIN, UserClass.USER, UserClass.GUEST]:
            u = make_user(f"u_{cls.lower()}", cls)
            self.client.force_login(u)
            self.assertEqual(self.client.get("/users/").status_code, 403)
            r = self.client.post("/users/", {"action": "save", "sel": [self.target.pk],
                                             f"class_{self.target.pk}": "ADMIN",
                                             f"status_{self.target.pk}": "APPROVED",
                                             f"version_{self.target.pk}": self.target.version})
            self.assertEqual(r.status_code, 403)
        self.target.refresh_from_db()
        self.assertEqual(self.target.id_status, IdStatus.REQUESTED)

    def test_main_shows_user_management_button_only_to_master(self):
        self.client.force_login(make_user("admin1", UserClass.ADMIN))
        self.assertNotContains(self.client.get("/"), "User Management")
        self.client.force_login(self.master)
        self.assertContains(self.client.get("/"), "User Management")

    def save(self, user, cls="GUEST", status="APPROVED", version=None):
        return self.client.post("/users/", {"action": "save", "sel": [user.pk],
                                            f"class_{user.pk}": cls, f"status_{user.pk}": status,
                                            f"version_{user.pk}": user.version if version is None else version})

    def test_master_approves_and_changes_class(self):
        self.client.force_login(self.master)
        self.save(self.target)
        self.target.refresh_from_db()
        self.assertEqual((self.target.user_class, self.target.id_status), (UserClass.GUEST, IdStatus.APPROVED))
        self.assertEqual(self.target.version, 2)

    def test_optimistic_lock_conflict_is_not_saved(self):
        self.client.force_login(self.master)
        stale = self.target.version
        User.objects.filter(pk=self.target.pk).update(version=stale + 1)  # 다른 사용자가 먼저 저장
        r = self.save(self.target, version=stale)
        self.target.refresh_from_db()
        self.assertEqual(self.target.id_status, IdStatus.REQUESTED)
        self.assertContains(self.client.get(r.url), "Another user changed this data first")

    def test_master_cannot_change_own_account_or_promote_to_master(self):
        self.client.force_login(self.master)
        self.save(self.master, cls="USER", status="DISABLED")
        self.master.refresh_from_db()
        self.assertEqual((self.master.user_class, self.master.id_status), (UserClass.MASTER, IdStatus.APPROVED))
        self.save(self.target, cls="MASTER")
        self.target.refresh_from_db()
        self.assertEqual(self.target.user_class, UserClass.USER)

    def test_4_password_reset_forces_change_before_using_modules(self):
        self.client.force_login(self.master)
        self.client.post("/users/", {"action": "reset", "sel": [self.target.pk]})
        User.objects.filter(pk=self.target.pk).update(id_status=IdStatus.APPROVED)
        self.assertEqual(len(mail.outbox), 1)
        temp = mail.outbox[0].body.split("password is: ")[1].split()[0]

        self.client.logout()
        r = self.client.post("/login/", {"username": "abydon", "password": temp})
        self.assertRedirects(r, "/me/")
        self.assertRedirects(self.client.get("/"), "/me/")  # 업무 화면 차단
        r = self.client.post("/me/", {"name": "Jordan", "email": "j@test.local", "tel": "",
                                      "old_password": temp, "new_password": "newpw2026", "new_password2": "newpw2026"})
        self.assertRedirects(r, "/")
        self.assertEqual(self.client.get("/").status_code, 200)
        self.target.refresh_from_db()
        self.assertFalse(self.target.must_change_password)
        self.assertTrue(self.target.check_password("newpw2026"))


class MyInfoTests(TestCase):
    def test_change_profile_without_password(self):
        u = make_user("nova007")
        self.client.force_login(u)
        self.client.post("/me/", {"name": "Emily", "email": "emily@test.local", "tel": "+84"})
        u.refresh_from_db()
        self.assertEqual((u.name, u.email), ("Emily", "emily@test.local"))
        self.assertTrue(u.check_password(PW))

    def test_password_change_needs_correct_old_password(self):
        u = make_user("nova007")
        self.client.force_login(u)
        r = self.client.post("/me/", {"name": "E", "email": "e@test.local", "old_password": "wrong999",
                                      "new_password": "newpw2026", "new_password2": "newpw2026"})
        self.assertContains(r, "Current password is incorrect")
        u.refresh_from_db()
        self.assertTrue(u.check_password(PW))


class CreateMasterCommandTests(TestCase):
    def test_creates_single_master_with_temporary_password(self):
        out = StringIO()
        call_command("create_master", "--email", "m@test.local", stdout=out)
        m = User.objects.get(username="novamaster")
        self.assertEqual((m.user_class, m.id_status, m.must_change_password), (UserClass.MASTER, IdStatus.APPROVED, True))
        temp = out.getvalue().split("(shown once): ")[1].split()[0]
        self.assertTrue(m.check_password(temp))
        with self.assertRaises(Exception):
            call_command("create_master", "--email", "m2@test.local", stdout=StringIO())
