from django.db import transaction
from django.shortcuts import get_object_or_404

from address.exceptions import AddressNotFoundException
from address.models import Address
from address.serializers import AddressSerializer


class AddressService:
    def __init__(self, address: Address = Address):
        self.address = address

    def get_my_address(self, user):
        return self.address.objects.filter(user=user)

    def get_address_by_id(self, user, address_id: int) -> Address:
        return get_object_or_404(Address, user=user, id=address_id)

    def get_default_address(self, user):
        return get_object_or_404(Address, user=user, default=True)

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
        exists_address = get_object_or_404(Address,
            id=address_id,
            user=user
        )

        for attr, value in serializer.validated_data.items():
            setattr(exists_address, attr, value)

        if exists_address.default:
            self.address.objects.filter(user=user).update(default=False)
        exists_address.save()


    @transaction.atomic
    def delete(self, user, address_id: int):
        address = self.address.objects.filter(id=address_id, user=user).first()
        if not address:
            raise AddressNotFoundException()
        address.delete()

    @transaction.atomic
    def set_default(self, user, address_id: int):
        self.address.objects.filter(user=user).update(default=False)
        address = get_object_or_404(Address, id=address_id, user=user)
        address.default = True
        address.save()
