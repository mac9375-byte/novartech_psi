from django import forms
from django.contrib.auth import password_validation

from .models import User
from .validators import normalize_username, validate_username


class LoginForm(forms.Form):
    username = forms.CharField(label="Purchaser ID", max_length=150)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class SignupForm(forms.Form):
    """Sign up (Ⅴ-3). 저장 시 Class=User, ID Status=Requested."""

    username = forms.CharField(label="Purchaser ID", max_length=150, strip=False)
    password = forms.CharField(label="P/W", widget=forms.PasswordInput, strip=False)
    password2 = forms.CharField(label="P/W Again", widget=forms.PasswordInput, strip=False)
    name = forms.CharField(label="Name", max_length=100)
    email = forms.EmailField(label="e-Mail")
    tel = forms.CharField(label="Tel", max_length=30, required=False)

    def clean_username(self):
        value = normalize_username(self.cleaned_data["username"])
        validate_username(value)
        if User.objects.filter(username=value).exists():
            raise forms.ValidationError("This Purchaser ID is already in use.")
        return value

    def clean(self):
        data = super().clean()
        pw, pw2 = data.get("password"), data.get("password2")
        if pw and pw2 and pw != pw2:
            self.add_error("password2", "P/W Again does not match.")
        if pw:
            try:
                password_validation.validate_password(pw)
            except forms.ValidationError as e:
                self.add_error("password", e)
        return data


class MyInfoForm(forms.Form):
    """ID Info Pop-up (Ⅴ-4-2): 본인 Name, e-mail, Tel, P/W 수정."""

    name = forms.CharField(label="Name", max_length=100)
    email = forms.EmailField(label="e-Mail")
    tel = forms.CharField(label="Tel", max_length=30, required=False)
    old_password = forms.CharField(label="Old P/W", widget=forms.PasswordInput, required=False, strip=False)
    new_password = forms.CharField(label="New P/W", widget=forms.PasswordInput, required=False, strip=False)
    new_password2 = forms.CharField(label="P/W Again", widget=forms.PasswordInput, required=False, strip=False)

    def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        if user.must_change_password:
            self.fields["old_password"].label = "Temporary P/W"

    def clean(self):
        data = super().clean()
        old, new, new2 = data.get("old_password"), data.get("new_password"), data.get("new_password2")
        changing = bool(old or new or new2) or self.user.must_change_password
        if not changing:
            return data
        if not new:
            self.add_error("new_password", "Enter a new password.")
        elif new != new2:
            self.add_error("new_password2", "P/W Again does not match.")
        else:
            try:
                password_validation.validate_password(new, self.user)
            except forms.ValidationError as e:
                self.add_error("new_password", e)
        if not old or not self.user.check_password(old):
            self.add_error("old_password", "Current password is incorrect.")
        elif new and old == new:
            self.add_error("new_password", "New password must be different.")
        data["changing_password"] = True
        return data
