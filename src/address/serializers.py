from rest_framework.serializers import ModelSerializer

from .models import Address
from .exceptions import AddressException


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

        extra_kwargs = {
            'id': {'read_only': True},
            'user_id': {'required': False, 'write_only': True}
        }

        
    def validate_phone(self, value):
        if not value.isdigit():
            raise AddressException.phoneNumberIsNotValid
        return value
