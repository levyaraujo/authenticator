from http import HTTPStatus

import jwt
from decouple import config
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Usuario
from .serializers import LoginSerializer, SignupSerializer


class Signup(APIView):
    def post(self, request):
        data = request.data
        try:
            Usuario.objects.get(email=data['email'])
            return Response({'error': 'this email is already registered'})
        except Exception as e:
            print(e)
        serializer = SignupSerializer(data=data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(
                serializer.validated_data['password'])
            serializer.save()
            return Response({'created': 'user successfully created'},
                            status=HTTPStatus.CREATED)
        return Response(serializer.errors)


class Login(APIView):
    def generate_token(self, email):
        token = RefreshToken.for_user(email)

        return {
            'refresh': str(token),
            'access': str(token.access_token),
        }

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        try:
            user = Usuario.objects.get(email=data['email'])
        except ObjectDoesNotExist as e:
            print(e)
            return Response({'not_exist': 'this email not exists'})

        if serializer.is_valid():
            if check_password(password=data['password'], encoded=user.password):  # noqa
                return Response(self.generate_token(user))
            return Response({'incorrect': 'password is incorrect'})
        return Response(serializer.errors)


class UserPage(APIView):
    permission_classes = [IsAuthenticated]

    def decode_jwt(self, request):
        try:
            header = request.headers['Authorization']
            token = header.split()[1]
            decoded = jwt.decode(token, config('jwt'), algorithms='HS256')
            return decoded['user_id']
        except Exception as e:
            print(e)
            return Response({'server_error': 'an error occurred'},
                            status=HTTPStatus.INTERNAL_SERVER_ERROR)

    def get(self, request):
        token = self.decode_jwt(request=request)
        try:
            user = Usuario.objects.get(id=token)
            data = {
                'name': user.name,
                'bio': user.bio,
                'email': user.email,
                'phone': user.phone,
                # 'photo': user.photo
            }
            print(user.photo)
            return Response({'data': data})

        except Exception as e:
            print(e)
            return Response('failed')
