import names
import pytest
from api.models import Usuario
from api.serializers import RegisterSerializer


class TestDatabase:
    @pytest.mark.django_db
    def test_users_endpoint(self):
        try:
            new_user = {
                "name": names.get_full_name(),
                "cpf": "05012119209",
                "password": "lima2409",
            }
            user = Usuario(**new_user)
            print(user)
            serializer = RegisterSerializer(data=new_user)
            if serializer.is_valid():
                user.save()
                return True
            print(serializer.errors)
            return False

        except Exception as e:
            print(e)
            return False
