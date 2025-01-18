from rest_framework.serializers import ModelSerializer

from .models import Address


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

        extra_kwargs = {
            'id': {'read_only': True},
            'user_id': {'required': False, 'write_only': True}
        }

        