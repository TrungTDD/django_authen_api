from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from ..serializers.user_serializer import UserRegisterSerializer
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from rest_framework import status
from ..utils.auth_util import generate_token, generate_access_token
import jwt
from django.conf import settings
from rest_framework import exceptions
# Create your views here.


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            if not User.objects.filter(username=username).exists():
                serializer.validated_data["password"] = make_password(password)
                user = serializer.save()
                access_token, refresh_token = generate_token(user)
                return Response(data={
                    "message": "Account create successfully",
                    "data" : {
                        "access_token" : access_token,
                        "refresh_token" : refresh_token,
                    }
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthView(APIView):
    def post(self, request):
        data = request.data
        username = data["username"]
        password = data["password"]

        if username is None or password is None:
            return Response(data={
                "message": "Username or password must required"
            }, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.filter(username=username).first()

        if user:
            is_valid_password = check_password(password, user.password)
            if is_valid_password:
                access_token, refresh_token = generate_token(user)
                return Response(data={
                    "message": "Login successfully",
                    "data": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "username": user.username
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response(data={
                    "message": "Invalid credential - Password is invalid"
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={
                "message": "Invalid credential - User not found"
            }, status=status.HTTP_401_UNAUTHORIZED)

    
    def put(self, request):
        data = request.data
        refresh_token = data.get("refresh_token", None)
        if not refresh_token:
            return Response(data={
                "message" : "Refresh Token must be required"
            }, status=status.HTTP_400_BAD_REQUEST)
        

        try:
            payload = jwt.decode(refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256'])
            if payload:
                user = User.objects.get(pk=payload['user_id'])
                token = generate_access_token(user)

                return Response(data={
                    "access_token": token
                }, status=status.HTTP_200_OK)
        except jwt.InvalidSignatureError:
            raise exceptions.AuthenticationFailed('refresh_token is invalid')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('refresh_token is expired')

