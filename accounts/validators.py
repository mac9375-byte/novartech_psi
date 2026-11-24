import re

from django.core.exceptions import ValidationError

USERNAME_RE = re.compile(r"^[a-z0-9._-]+$")


def normalize_username(value):
    """ID: 앞뒤 공백 제거 + 소문자 (H-2)."""
    return (value or "").strip().lower()


def validate_username(value):
    """ID: 영문·숫자·'.'·'_'·'-'만, 중간 공백 불가 (Ⅴ-3-1, H-2). value는 정규화된 값."""
    if not value:
        raise ValidationError("Purchaser ID is required.")
    if not USERNAME_RE.match(value):
        raise ValidationError("Only letters, numbers and . _ - are allowed (no spaces).")


class NovatechPasswordValidator:
    """P/W: 8자 이상, 영문·숫자 각 1자 이상, 공백 불가, 특수문자 선택 (Ⅴ-1-7)."""

    def validate(self, password, user=None):
        errors = []
        if len(password) < 8:
            errors.append("Password must be at least 8 characters.")
        if not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password):
            errors.append("Password must include at least one letter and one number.")
        if re.search(r"\s", password):
            errors.append("Password must not contain spaces.")
        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        return "8+ characters, at least one letter and one number, no spaces."
