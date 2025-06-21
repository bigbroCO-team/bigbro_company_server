import requests
from django.conf import settings
from django.db.models import Sum
from rest_framework import serializers

from product.serializers import ProductReadSerializer
from .models import Order, OrderItem


class OrderPatchSerializer(serializers.Serializer):
    address = serializers.CharField()
    request = serializers.CharField()


class OrderItemWriteSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    option = serializers.CharField()
    quantity = serializers.IntegerField()


class OrderWriteSerializer(serializers.Serializer):
    products = OrderItemWriteSerializer(many=True)


class OrderItemReadSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer()
    product_option = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_option', 'quantity', 'status', 'price')

    def get_product_option(self, obj):
        return obj.product_option.name


class OrderReadSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, source='order_item')
    delivery_status = serializers.SerializerMethodField(allow_null=True)
    product_total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id', 'total_price', 'tracking_number', 'delivery_company',
            'address', 'address_detail', 'zipcode', 'request', 'phone',
            'items', 'delivery_status', 'delivery_cost', 'product_total_price'
        )

    def get_delivery_status(self, obj):
        if not obj.tracking_number:
            return None

        return requests.get(
            f'{settings.DELIVERY_TRAKER_API}/carriers/kr.logen/tracks/{obj.tracking_number}',
        ).json().get('state').get('text')

    def get_product_total_price(self, obj):
        return obj.order_item.aggregate(
            total=Sum('price')
        ).get('total')