from typing import List

from rest_framework import serializers

from .models import Usuario


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields: List[str] = ["name", "cpf", "password", "role"]


class ChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields: List[str] = ["name", "password", "role"]


class LoginSerializer(serializers.Serializer):
    cpf = serializers.CharField(max_length=70)
    password = serializers.CharField(max_length=100)
