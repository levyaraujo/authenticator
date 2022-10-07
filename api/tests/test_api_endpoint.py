import json

import names
import pytest
from api.serializers import RegisterSerializer
from rest_framework import status
from rest_framework.test import APITestCase


class TestAPI(APITestCase):
    @pytest.mark.django_db
    def test_register_page(self):
        user = {
            "name": names.get_full_name(),
            "cpf": "1234567890",
            "password": "12345",
        }

        serializer = RegisterSerializer(data=user)
        if serializer.is_valid():
            response = self.client.post(
                "/register/",
                json.dumps(user),
                content_type="application/json",
            )
            print(response.content)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(serializer.errors)

    def test_login_page(self):
        response = self.client.post(
            "/login/",
            data=json.dumps({"cpf": "05012119266", "password": "lima2409"}),
            content_type="application/json",
        )
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
