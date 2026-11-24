"""Master 계정(novamaster) 최초 생성 (Ⅴ-1-1).

임시 P/W를 무작위로 만들어 이 화면에 한 번만 보여준다. 소스코드에 P/W를 두지 않는다.
최초 Log-in 시 새 P/W로 변경해야 한다.
"""
from django.core.management.base import BaseCommand, CommandError

from accounts.models import IdStatus, User, UserClass
from accounts.views import _new_temp_password

MASTER_ID = "novamaster"


class Command(BaseCommand):
    help = "Create the single Master account (novamaster) with a temporary password."

    def add_arguments(self, parser):
        parser.add_argument("--email", required=True, help="Master e-mail address")
        parser.add_argument("--name", default="Master")

    def handle(self, *args, **opts):
        if User.objects.filter(user_class=UserClass.MASTER).exists():
            raise CommandError("A Master account already exists.")
        temp = _new_temp_password()
        User.objects.create_user(
            MASTER_ID, temp, name=opts["name"], email=opts["email"],
            user_class=UserClass.MASTER, id_status=IdStatus.APPROVED, must_change_password=True,
        )
        self.stdout.write(f"Master ID: {MASTER_ID}")
        self.stdout.write(f"Temporary password (shown once): {temp}")
        self.stdout.write("Log in and set a new password.")
