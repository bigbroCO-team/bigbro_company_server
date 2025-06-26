from django.db import models

from accounts.models import User
from address.exceptions import AddressTooManyDefaultFieldException
from core.basemodel import BaseModel


class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="address")
    name = models.CharField(max_length=17)
    phone = models.CharField(max_length=11)
    tag = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=10)
    address = models.TextField()
    detail = models.CharField(max_length=50)
    default = models.BooleanField(default=False)

    class Meta:
        db_table = "address"

    def clean(self):
        if self.default:
            address_default_count = (
                Address.objects.filter(user=self.user).values("default").exists()
            )
            if address_default_count:
                raise AddressTooManyDefaultFieldException()
