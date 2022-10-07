from http import HTTPStatus

import jwt
from decouple import config
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Usuario
from .serializers import ChangeSerializer, LoginSerializer, RegisterSerializer


class Register(APIView):
    def post(self, request):
        data = request.data
        print(data)
        serializer = RegisterSerializer(data=data)
        try:
            Usuario.objects.exclude(cpf=data["cpf"])
            if serializer.is_valid():
                serializer.validated_data["password"] = make_password(
                    serializer.validated_data["password"]
                )
                serializer.save()
                return Response(
                    {"created": "User successfully created"},
                    status=HTTPStatus.CREATED,  # noqa
                )
            return Response(serializer.errors)

        except Exception as e:
            print(e)
            return Response({"error": "An error occurred trying to save user"})


class Login(APIView):
    def generate_token(self, cpf):
        token = RefreshToken.for_user(cpf)

        return {
            "refresh": str(token),
            "access": str(token.access_token),
        }

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        try:
            user = Usuario.objects.get(cpf=data["cpf"])
            if serializer.is_valid():
                if check_password(
                    password=data["password"], encoded=user.password
                ):  # noqa
                    return Response(self.generate_token(user), 200)

                return Response(
                    {"incorrect": "password is incorrect"}, HTTPStatus.UNAUTHORIZED
                )
        except ObjectDoesNotExist as e:
            print(e)
            return Response(
                {"not_exist": "cpf not exists"}, HTTPStatus.UNAUTHORIZED
            )  # noqa

        return Response(serializer.errors)


class UserPage(APIView):
    permission_classes = [IsAuthenticated]

    def decode_jwt(self, request):
        try:
            header = request.headers["Authorization"]
            token = header.split()[1]
            decoded = jwt.decode(token, config("jwt"), algorithms="HS256")
            return decoded["user_id"]
        except Exception as e:
            print(e)
            return Response(
                {"server_error": "An error occurred"},
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    def get(self, request):
        token = self.decode_jwt(request=request)
        try:
            user = Usuario.objects.get(id=token)
            all_users = Usuario.objects.all()
            users = []
            print(users)

            for user in all_users:
                users.append({"id": user.id, "name": user.name})

            return Response({"users": users})

        except ObjectDoesNotExist as e:
            print(e)
            return Response(
                {"not_exists": "The requested resource does not exist"},
                HTTPStatus.NOT_FOUND,
            )

        except PermissionDenied as e:
            print(e)
            return Response(
                {"denied": "You don't have permission to perform this action"},
                HTTPStatus.UNAUTHORIZED,
            )

    def patch(self, request, id):
        data = request.data
        serializer = ChangeSerializer(data=data, partial=True)
        token = self.decode_jwt(request)
        logged_user = Usuario.objects.get(id=token)

        try:
            if logged_user.role == "A":
                if serializer.is_valid(raise_exception=True):
                    data["password"] = make_password(data["password"])
                    user = Usuario.objects.filter(id=id)
                    user.update(**data)
                    return Response(
                        {"success": "User successfully updated"}, HTTPStatus.OK
                    )
                return Response(serializer.errors)

            return Response(
                {"unauthorized": "You don't have permission to perform this action"}
            )

        except KeyError as e:
            print(e)
            return Response({"field_required": f"The {e} field is required"})

        except Usuario.DoesNotExist:
            return Response({"not_found": "User does not exists"}, HTTPStatus.NOT_FOUND)
