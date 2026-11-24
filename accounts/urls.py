from django.urls import path

from . import views

urlpatterns = [
    path("", views.main_view, name="main"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("signup/check-id/", views.check_id_view, name="check_id"),
    path("me/", views.me_view, name="me"),
    path("users/", views.users_view, name="users"),
]
