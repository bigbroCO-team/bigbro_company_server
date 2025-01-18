from django.db import models

from accounts.models import User


class Address(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address_id')
    name = models.CharField(max_length=17)
    phone = models.CharField(max_length=11)
    tag = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=10)
    address = models.TextField()
    detail = models.CharField(max_length=50)
    request = models.TextField()

    class Meta:
        db_table = 'address'