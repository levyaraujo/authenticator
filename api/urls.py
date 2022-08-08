from typing import List

from django.urls import path

from .views import Login, Signup

urlpatterns: List = [
    path('signup/', Signup.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
]
