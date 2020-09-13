from django.contrib.auth.models import User
from django.utils import timezone

import jwt
from rest_framework import authentication


JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_SECONDS = 60
JWT_SECRET = 'ASDF'


def generate_jwt_token(user):
    payload = {
        'username': user.username,
        'exp': timezone.now() + timezone.timedelta(seconds=JWT_EXPIRATION_SECONDS)
    }
    return jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return None
        else:
            return (User.objects.get(username=payload.get('username')), None)
