from django.urls import path
from . import views

urlpatterns = [
    path("me/", views.me, name="setting-me"),
    path("me/password/", views.change_password, name="setting-change-password"),
    path("auth/login/", views.login_view, name="setting-login"),
    path("auth/logout/", views.logout_view, name="setting-logout"),
]
