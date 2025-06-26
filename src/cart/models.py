from django.db import models

from accounts.models import User
from core.basemodel import BaseModel
from product.models import Product, ProductOption


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=False
    )
    option = models.ForeignKey(
        ProductOption, on_delete=models.SET_NULL, null=True, blank=False
    )
    count = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "cart"
        unique_together = ["user", "product", "option"]

    def __str__(self):
        return str(self.id)
