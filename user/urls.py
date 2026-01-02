from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage_view, name="homepage"),
    path("signup", views.signup_view, name="signup"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]