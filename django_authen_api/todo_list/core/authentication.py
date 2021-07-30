from django.contrib.auth.models import User
from rest_framework import authentication
import jwt
from django.conf import settings
from rest_framework import exceptions


class MyJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token_header = request.META.get("HTTP_AUTHORIZATION")

        if not token_header:
            return None

        try:
            # header: Bearer xxxxxxx
            access_token = token_header.split(' ')[1]

            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.InvalidSignatureError:
            raise exceptions.AuthenticationFailed('access_token is invalid')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        user = User.objects.filter(id=payload['user_id']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        return (user, None)
