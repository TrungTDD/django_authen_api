import datetime
from datetime import timedelta

import jwt
from django.conf import settings


def generate_token(user):
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    return (access_token, refresh_token)


def generate_access_token(user):
    token_payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.datetime.now() + timedelta(minutes=60),
        "iat": datetime.datetime.now(),
    }

    access_token = jwt.encode(
        token_payload, settings.SECRET_KEY, algorithm="HS256"
    ).decode("utf-8")
    return access_token


def generate_refresh_token(user):
    token_payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.datetime.now() + timedelta(days=7),
        "iat": datetime.datetime.now(),
    }

    access_token = jwt.encode(
        token_payload, settings.REFRESH_TOKEN_SECRET, algorithm="HS256"
    ).decode("utf-8")
    return access_token
