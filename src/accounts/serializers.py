from rest_framework import serializers

from accounts.exceptions import PasswordTooShortException
from accounts.models import User
from address.serializers import AddressSerializer


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        if len(value) < 6:
            raise PasswordTooShortException()
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class MyInfoSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'address')