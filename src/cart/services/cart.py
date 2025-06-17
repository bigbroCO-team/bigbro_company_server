from django.db import transaction
from django.shortcuts import get_object_or_404

from cart.models import Cart
from cart.serilaizers import CartWriteSerializer
from product.models import Product


class CartService:
    def __init__(
            self,
            cart: Cart = Cart,
            product: Product = Product,
    ):
        self.cart = cart
        self.product = product

    def get_my_cart_list(self, user):
        return self.cart.objects.filter(user=user).select_related('product', 'option')

    @transaction.atomic
    def save(self, user, serializer: CartWriteSerializer):
        # 기존 Cart 조회
        exists_cart = self.cart.objects.filter(
            user=user,
            product=serializer.validated_data.get('product'),
            option=serializer.validated_data.get('option')
        ).first()

        # 기존 cart가 있다면 count 증가, 없다면 생성
        if exists_cart:
            exists_cart.count += serializer.validated_data.get('count')
            exists_cart.save()
        else:
            new_cart = Cart(
                user=user,
                **serializer.validated_data,
            )
            new_cart.save()

    @transaction.atomic
    def delete(self, user, cart_id: int):
        get_object_or_404(Cart, user=user, id=cart_id).delete()