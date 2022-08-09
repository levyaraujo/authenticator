from typing import List

from rest_framework import serializers

from .models import Usuario


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields: List[str] = ['name', 'email', 'password']


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=70)
    password = serializers.CharField(max_length=100)
