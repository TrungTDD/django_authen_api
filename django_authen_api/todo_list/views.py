from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers.user_serializer import UserRegisterSerializer
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from rest_framework import status
from .utils.auth_util import issue_token
# Create your views here.


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            if not User.objects.filter(username=username).exists():
                serializer.validated_data["password"] = make_password(password)
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        data = request.data
        username = data["username"]
        password = data["password"]
        if User.objects.filter(username=username).exists():
            user = authenticate(request, username=username,
                                password=password)
            if user:
                auth_result = issue_token(user)
                return Response(data=auth_result, status=status.HTTP_200_OK)

        return Response(data={
            "message": "Credential is not valid"
        }, status=status.HTTP_400_BAD_REQUEST)


class TodoView(APIView):
    pass
