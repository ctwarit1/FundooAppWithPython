import jwt
from django.conf import settings
from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.response import Response

from user.models import User


def encode(payload):
    if "exp" not in payload.keys():
        payload.update(exp=datetime.utcnow() + timedelta(hours=1))
    return jwt.encode(payload, settings.SECRET, algorithm=settings.ALGORITHMS)


def decode(token):
    try:
        return jwt.decode(token, settings.SECRET, algorithms=[settings.ALGORITHMS])
    except jwt.PyJWTError as ex:
        raise Exception(ex)



def authenticate_user(function):
    def wrapper(self, request):
        token = request.headers.get("token")
        if not token:
            return Response({"message": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)
        decoded = decode(token)
        if not decoded:
            return Response({"message": "Token Authentication required"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=decoded.get("user"))
        if not user:
            return Response({"message": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)
        request.data.update({"user": user.id})
        return function(self, request)
    return wrapper

