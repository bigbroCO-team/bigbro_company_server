from rest_framework import serializers

from accounts.models import User
from accounts.exceptions import AccountException


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise AccountException.UserNameAlreadyExistsException
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise AccountException.PasswordTooShortException
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)