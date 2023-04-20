from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.response import Response

from user.utils import encode, decode
from user.models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'location', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    def create(self, validated_data):
        user = authenticate(username=validated_data['username'], password=validated_data['password'])

        if not user:
            raise Exception("Invalid Credentials")
        if not user.is_verified:
            raise Exception("User Not Verified")
        token = encode({"user": user.id})
        self.context.update({"token": token})
        return user
