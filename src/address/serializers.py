from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[RegexValidator(regex=r"^\d{10,11}$")])

    class Meta:
        model = Address
        fields = (
            "id",
            "tag",
            "name",
            "zipcode",
            "phone",
            "address",
            "detail",
            "default",
        )
