from django.db import transaction
from django.shortcuts import get_object_or_404

from address.exceptions import AddressNotFoundException
from address.models import Address
from order.exceptions import OrderNotFoundException
from order.models import Order, OrderItem
from order.serializers import OrderWriteSerializer
from product.exceptions import ProductNotFoundException, OptionNotFoundException
from product.models import Product, ProductOption


class OrderService:
    def __init__(
            self,
            order: Order = Order,
            address: Address = Address,
            product: Product = Product,
            product_option: ProductOption = ProductOption,
            order_item: OrderItem = OrderItem
    ):
        self.order = order
        self.address = address
        self.product = product
        self.product_option = product_option
        self.order_item = order_item

    def get_my_order_by_id(self, user, order_id):
        order = self.order.objects.filter(user=user).prefetch_related('order_item')
        if not order:
            raise OrderNotFoundException()

    def get_my_order_list(self, user):
        return self.order.objects.filter(user=user).prefetch_related('order_item')

    @transaction.atomic
    def create(self, user, serializer: OrderWriteSerializer):
        products = serializer.validated_data.pop('products')
        address = serializer.validated_data.pop('address')
        total_price = 0

        # Get address
        address = get_object_or_404(Address, id=address)

        # Create order
        order = Order.objects.create(
            user=user,
            address=address.address,
            address_detail=address.detail,
            zipcode=address.zipcode,
            request=address.request,
            phone=address.phone,
        )

        # Create order items
        order_items = []
        for _product in products:
            # Product, Option 조회
            product = get_object_or_404(Product, id=_product['product'])
            option = get_object_or_404(ProductOption, name=_product['option'])

            # order.total_price 계산
            total_price += (product.price - int(product.price * product.discount / 100)) * _product['quantity']

            # order item 추가
            order_items.append(
                OrderItem(
                    product=product,
                    product_option=option,
                    order=order,
                    quantity=_product['quantity'],
                    price=product.price,  # 추후 item에 가격 변동시 조정 필요
                )
            )

        self.order_item.objects.bulk_create(order_items)

        order.total_price = total_price
        order.save()

        return order