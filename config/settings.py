"""Material PSI 분석 도우미 - Django settings (Local PoC)."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _read_env(path):
    # ponytail: 'KEY=VALUE' 줄만 읽는 최소 파서. 따옴표·여러 줄 값이 필요해지면 python-dotenv로 교체
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip()
    return env


ENV = _read_env(BASE_DIR / ".env")

SECRET_KEY = ENV["DJANGO_SECRET_KEY"]
DEBUG = ENV.get("DJANGO_DEBUG") == "1"
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "core",
    "materials",
    "assies",
    "bom",
    "safety",
    "weekly",
    "psi",
]

# Material Master 등 표 화면의 한 번 저장 시 입력칸 수 상한 (기본 1,000은 1,000행 표에 부족)
DATA_UPLOAD_MAX_NUMBER_FIELDS = 20000

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # 로그인하지 않은 요청은 모두 Log-in 화면으로 (예외: @login_not_required 화면)
    "django.contrib.auth.middleware.LoginRequiredMiddleware",
    "accounts.middleware.ForcePasswordChangeMiddleware",
    "accounts.middleware.UserTimezoneMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": ENV.get("DB_NAME", "novatech_psi"),
        "USER": ENV.get("DB_USER", "novatech_app"),
        "PASSWORD": ENV.get("DB_PASSWORD", ""),
        "HOST": ENV.get("DB_HOST", "localhost"),
        "PORT": ENV.get("DB_PORT", "5432"),
        # DB가 꺼져 있으면 무한 대기하지 않고 5초 후 오류 표시
        "OPTIONS": {"connect_timeout": 5},
    }
}

AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"

# Password는 Hash로만 저장 (Django 기본 PBKDF2). 규칙 검사는 accounts.validators (Ⅴ-1-7)
AUTH_PASSWORD_VALIDATORS = [{"NAME": "accounts.validators.NovatechPasswordValidator"}]

# Session: 2시간 미사용 시 자동 Log-out (요청마다 만료시각 연장) (Ⅴ-1-7)
SESSION_COOKIE_AGE = 2 * 60 * 60
SESSION_SAVE_EVERY_REQUEST = True

# 시간: DB는 UTC 저장. 화면은 브라우저 Timezone, 모를 때는 베트남 Business Timezone (Ⅳ-6-4)
USE_TZ = True
TIME_ZONE = "Asia/Ho_Chi_Minh"
LANGUAGE_CODE = "en-us"
USE_I18N = True

# PoC: 메일을 실제로 보내지 않고 runserver 터미널에 출력. 운영 전환 시 SMTP 설정으로 교체 (Ⅴ-5, 권장안 승인)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@novatech.local"

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
