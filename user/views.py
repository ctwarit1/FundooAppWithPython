import json

from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from logger import logger

from user.models import User
from user.serializers import UserSerializers, UserLoginSerializers


class UserReg(APIView):

    def post(self, request):
        try:
            serializer = UserSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "User registration Successful", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": e})


class UserLogin(APIView):

    def post(self, request):
        try:
            serializer = UserLoginSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Login Successful", "status": 202, "data": {}},
                            status=status.HTTP_202_ACCEPTED)



        except Exception as e:
            return Response({"message": e.args[0]})
