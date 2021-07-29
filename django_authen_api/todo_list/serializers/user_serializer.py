from rest_framework import serializers
from django.contrib.auth.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    # currently for demo purposing, only uusing user name and password
    class Meta:
        model = User
        fields = ('username', 'password')
