from django.db import models
from django.shortcuts import get_object_or_404

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
        unique_together = ("user", "product", "option")

    @classmethod
    def add_count_or_create(cls, user: User, data):
        exists_cart = Cart.objects.filter(
            user=user,
            product=data.get("product"),
            option=data.get("option"),
        ).first()

        if exists_cart:
            exists_cart.count += data.get("count")
            exists_cart.save()
        else:
            Cart(user=user, **data).save()
