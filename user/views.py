import token

from .models import User
from .utils import encode, decode
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from logger import logger
from user.serializers import UserSerializers, UserLoginSerializers
from rest_framework.reverse import reverse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UserReg(APIView):

    @swagger_auto_schema(request_body=UserSerializers)
    def post(self, request):
        try:
            serializer = UserSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            token = encode({"user": serializer.data.get("id")})
            link = f"{settings.BASE_URL}{reverse('verify_user')}?token={token}"
            send_mail(
                subject='Verify token',
                message=link,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[serializer.data.get("email")],
            )
            return Response({"message": "User registration Successful", "status": 201,
                             "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):

    @swagger_auto_schema(request_body=UserLoginSerializers)
    def post(self, request):
        try:
            serializer = UserLoginSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Login Successful", "status": 202, "data": serializer.context.get("token")},
                            status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)


class VerifyUser(APIView):
    @swagger_auto_schema(manual_parameters=[openapi.Parameter('token', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                                                              required=True)])
    def get(self, request):
        payload = decode(token=request.query_params.get("token"))
        user = User.objects.get(id=payload.get("user"))
        if not user:
            raise Exception("Invalid user")
        user.is_verified = True
        user.save()
        return Response({"message": "User Verified", "status": 202, "data": {}},
                        status=status.HTTP_202_ACCEPTED)
