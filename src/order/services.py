from django.shortcuts import get_object_or_404

from order.models import Order, OrderItem
from order.serializers import OrderWriteSerializer
from product.models import Product, ProductOption


def create_order(user, serializer: OrderWriteSerializer):
    products = serializer.validated_data.pop("products")
    total_price = 0

    # Create order
    order = Order.objects.create(
        user=user,
    )

    # Create order items
    order_items = []
    for _product in products:

        # Product, Option 조회
        product = get_object_or_404(Product, id=_product["product"])
        option = get_object_or_404(
            ProductOption, name=_product["option"], product=product
        )

        # order.total_price 계산
        total_price += (
            product.price - int(product.price * product.discount / 100)
        ) * _product["quantity"]

        # order item 추가
        order_items.append(
            OrderItem(
                product=product,
                product_option=option,
                order=order,
                quantity=_product["quantity"],
                price=product.price,  # 추후 item에 가격 변동시 조정 필요
            )
        )

    OrderItem.objects.bulk_create(order_items)

    # 배송비 계산
    delivery_cost = order.delivery_cost if total_price < 50000 else 0
    order.delivery_cost = delivery_cost
    order.total_price = total_price + delivery_cost

    order.save()
