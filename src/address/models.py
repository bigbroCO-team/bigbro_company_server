from django.db import models


class Address(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=17)
    phone = models.CharField(max_length=11)
    tag = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=10)
    address = models.TextField()
    detail = models.CharField(max_length=50)
    request = models.TextField()

    class Meta:
        db_table = 'address'