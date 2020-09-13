from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, authentication_classes, parser_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .utils import generate_jwt_token, JWTAuthentication


@api_view(['POST'])
@parser_classes([JSONParser])
def login(request, format=None):
    user = authenticate(
        username=request.data.get('username'),
        password=request.data.get('password'),
    )
    if user:
        return Response({'token': generate_jwt_token(user)})
    else:
        return Response({'status': 'KO: Wrong credentials.'}, status=400)


@api_view(['POST'])
@parser_classes([JSONParser])
def signup(request, format=None):
    User.objects.create_user(
        request.data.get('username'),
        password=request.data.get('password'),
    )
    return Response({'status': 'ok'})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def protected(request, format=None):
    return Response({'status': 'ok'})
