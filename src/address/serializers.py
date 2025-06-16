import re

from rest_framework.serializers import ModelSerializer

from .exceptions import PhoneNumberIsNotValidException
from .models import Address


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'tag', 'name', 'zipcode', 'phone', 'address', 'detail', 'default')

    def validate_phone(self, value):
        if not re.fullmatch(r'^\d{10,11}$', value):
            raise PhoneNumberIsNotValidException()
        return value
