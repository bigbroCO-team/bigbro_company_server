from django.db import transaction
from django.shortcuts import get_object_or_404

from cart.models import Cart
from product.models import ProductOption


class CartService:
    def __init__(self):
        pass

    @transaction.atomic
    def create(self, user, product, option, count):

        option_obj = get_object_or_404(ProductOption,
            product_id=product,
            name=option
        )

        exists_cart = Cart.object.filter(
            user=user,
            product=product,
            option=option_obj
        ).first()

        if exists_cart:
            exists_cart.count += count
            exists_cart.save()
            return exists_cart
        else:
            new_cart = Cart(
                user=user,
                product=product,
                option=option_obj,
                count=count
            )
            new_cart.full_clean()
            new_cart.save()
            return new_cart