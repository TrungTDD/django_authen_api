import jwt
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.user_serializer import UserRegisterSerializer
from ..utils.auth_util import generate_access_token, generate_token

# Create your views here.


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        password = serializer.validated_data["password"]
        serializer.validated_data["password"] = make_password(password)
        user = serializer.save()
        access_token, refresh_token = generate_token(user)
        res = {
            "message": "Account create successfully",
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
        }

        return Response(data=res, status=status.HTTP_201_CREATED)


class AuthView(APIView):
    def post(self, request):
        data = request.data
        username = data["username"]
        password = data["password"]

        if username is None or password is None:
            return Response(
                data={"message": "Username or password must required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = User.objects.filter(username=username).first()

        if user:
            is_valid_password = check_password(password, user.password)
            if is_valid_password:
                access_token, refresh_token = generate_token(user)
                return Response(
                    data={
                        "message": "Login successfully",
                        "data": {
                            "access_token": access_token,
                            "refresh_token": refresh_token,
                            "username": user.username,
                        },
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    data={"message": "Invalid credential - Password is invalid"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(
                data={"message": "Invalid credential - User not found"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def put(self, request):
        data = request.data
        refresh_token = data.get("refresh_token", None)
        if not refresh_token:
            return Response(
                data={"message": "Refresh Token must be required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            payload = jwt.decode(
                refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=["HS256"]
            )
            if payload:
                user = User.objects.get(pk=payload["user_id"])
                token = generate_access_token(user)

                return Response(data={"access_token": token}, status=status.HTTP_200_OK)
        except jwt.InvalidSignatureError:
            raise exceptions.AuthenticationFailed("refresh_token is invalid")
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("refresh_token is expired")
