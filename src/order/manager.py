from django.db import models, transaction
from django.shortcuts import get_object_or_404

from order.models import Order, OrderItem
from product.models import Product, ProductOption


class OrderManager(models.Manager):
    @transaction.atomic
    def create_order(self, user, validated_data):
        total_price = 0

        # 주문 생성
        order = Order.objects.create(user=user)

        # 주문 아이템 생성
        order_items = []
        for p in validated_data.get("products"):
            product = get_object_or_404(Product, id=p.get("product"))
            option = get_object_or_404(
                ProductOption, name=p.get("option"), product=product
            )

            total_price += (
                product.price - int(product.price * product.discount / 100)
            ) * p.get("quantity")

            order_items.append(
                OrderItem(
                    product=product,
                    product_option=option,
                    order=order,
                    quantity=p.get("quantity"),
                    price=product.price,
                )
            )

        OrderItem.objects.bulk_create(order_items)

        # 배송비 계산
        delivery_cost = order.delivery_cost if total_price < 50000 else 0

        order.delivery_cost = delivery_cost
        order.total_price = total_price + delivery_cost
        order.save()
