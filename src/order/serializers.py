import requests
from django.conf import settings
from rest_framework import serializers

from product.serializers import ProductReadSerializer, ProductOptionSerializer
from .models import Order, OrderItem


class OrderItemWriteSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    option = serializers.CharField()
    quantity = serializers.IntegerField()


class OrderWriteSerializer(serializers.Serializer):
    products = OrderItemWriteSerializer(many=True)
    address = serializers.IntegerField()
    request = serializers.CharField()


class OrderItemReadSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer()
    product_option = ProductOptionSerializer()

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_option', 'quantity', 'status', 'price')


class OrderReadSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, source='order_item')
    delivery_status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id', 'total_price', 'tracking_number', 'delivery_company',
            'address', 'address_detail', 'zipcode', 'request', 'phone',
            'items', 'delivery_status'
        )

    def get_delivery_status(self, obj):
        if not obj.tracking_number:
            return "배송 준비 중"

        return requests.get(
            f'{settings.DELIVERY_TRAKER_API}/carriers/kr.logen/tracks/{obj.tracking_number}',
        ).json().get('state').get('text')