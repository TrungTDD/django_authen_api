from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings


def issue_token(user):
    refresh = TokenObtainPairSerializer.get_token(user)
    return {
        'refresh': str(refresh),
        'token': str(refresh.access_token),
        'access_expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
        'refresh_expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
    }
