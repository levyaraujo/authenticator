from typing import List

from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from .views import Login, Register, UserPage

urlpatterns: List = [
    path("register", Register.as_view(), name="register"),
    path("login", Login.as_view(), name="login"),
    path("users", UserPage.as_view(), name="user_page"),
    path("users/edit/<int:id>", UserPage.as_view(), name="user_page"),
    path("token/verify", TokenVerifyView.as_view(), name="token_verify"),
]
