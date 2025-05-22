from django.db import transaction
from rest_framework.request import Request

from address.exceptions import AddressNotFoundException
from address.models import Address
from address.serializers import AddressSerializer


class AddressService:
    def __init__(self, address: Address = Address):
        self.address = address

    def get_my_address(self, request: Request):
        return self.address.objects.filter(user=request.user)

    def get_default_address(self, request: Request):
        return self.address.objects.get(user=request.user, default=True)

    @transaction.atomic
    def save(self, user, serializer: AddressSerializer):
        address = Address(
            user=user,
            **serializer.validated_data,
        )
        address.full_clean()
        address.save()

    @transaction.atomic
    def update(self, user, address_id: int, serializer: AddressSerializer):
        exists_address = self.address.objects.get(
            id=address_id,
            user=user
        )
        exists_address.full_clean()
        serializer.instance = exists_address
        serializer.save()

    @transaction.atomic
    def delete(self, user, address_id: int):
        address = Address.objects.filter(id=address_id, user=user).first()
        if not address:
            raise AddressNotFoundException()
        address.delete()