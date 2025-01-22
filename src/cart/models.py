from django.db import models

from accounts.models import User
from product.models import Product, ProductOption


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'cart'

    def __str__(self):
        return str(self.id)