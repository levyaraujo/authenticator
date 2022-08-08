from typing import List

from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)
    bio = models.TextField()
    phone = models.CharField(max_length=9)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='api/images')
    REQUIRED_FIELDS: List = []
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name
