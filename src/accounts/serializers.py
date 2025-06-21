from django.core.validators import MinLengthValidator
from rest_framework import serializers

from accounts.models import User
from address.serializers import AddressSerializer


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(
        write_only=True,
        validators=[MinLengthValidator(6)]
    )


class MyInfoSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=True)
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'address', 'role')

    def get_role(self, obj):
        return "STAFF" if obj.is_staff else "USER"