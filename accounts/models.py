from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserClass(models.TextChoices):
    MASTER = "MASTER", "Master"
    ADMIN = "ADMIN", "Admin"
    USER = "USER", "User"
    GUEST = "GUEST", "Guest"


class IdStatus(models.TextChoices):
    REQUESTED = "REQUESTED", "Requested"
    APPROVED = "APPROVED", "Approved"
    DISABLED = "DISABLED", "Disabled"


class UserManager(BaseUserManager):
    def create_user(self, username, password, **fields):
        user = self.model(username=username.strip().lower(), **fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    """사용자 계정 (Ⅴ-1). username = Purchaser ID."""

    username = models.CharField("Purchaser ID", max_length=150, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField("e-Mail", max_length=254)
    tel = models.CharField(max_length=30, blank=True)
    user_class = models.CharField("Class", max_length=10, choices=UserClass.choices, default=UserClass.USER)
    id_status = models.CharField("ID Status", max_length=10, choices=IdStatus.choices, default=IdStatus.REQUESTED)
    must_change_password = models.BooleanField(default=False)
    failed_login_count = models.PositiveSmallIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    password_reset_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.PositiveIntegerField(default=1)  # Optimistic Lock (Ⅰ-11)

    objects = UserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name", "email"]

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return self.username

    @property
    def is_master(self):
        return self.user_class == UserClass.MASTER
