import requests
from django.conf import settings
from django.db.models import Sum
from rest_framework import serializers

from address.models import Address
from product.serializers import ProductReadSerializer
from .enums import OrderStatus
from .models import Order, OrderItem


class OrderUpdateSerializer(serializers.Serializer):
    address = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(),
    )
    request = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        address = validated_data.get("address")
        request = validated_data.get("request")

        instance.name = address.name
        instance.zipcode = address.zipcode
        instance.address = address.address
        instance.address_detail = address.detail
        instance.phone = address.phone
        instance.request = request

        instance.save()
        return instance


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
        fields = ("id", "product", "product_option", "quantity", "price")

    def get_product_option(self, obj):
        return obj.product_option.name if obj.product_option else None


class OrderReadAddressSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone = serializers.CharField()
    zipcode = serializers.CharField()
    address = serializers.CharField()
    address_detail = serializers.CharField()
    request = serializers.CharField(allow_blank=True)


class OrderReadSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, source="order_item")
    delivery_status = serializers.SerializerMethodField(allow_null=True)
    product_total_price = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id",
            "total_price",
            "tracking_number",
            "delivery_company",
            "delivery_cost",
            "status",
            "receipt_url",
            "items",
            "delivery_status",
            "product_total_price",
            "address",
            "created_at",
        )

    def get_delivery_status(self, obj):
        response = requests.get(
            f"{settings.DELIVERY_TRAKER_API}/carriers/kr.logen/tracks/{obj.tracking_number or ""}",
        )

        if response.status_code == 200:
            return response.json().get("state").get("text")
        else:
            return None

    def get_product_total_price(self, obj):
        return obj.order_item.aggregate(total=Sum("price")).get("total")

    def get_address(self, obj):
        return OrderReadAddressSerializer(
            {
                "name": obj.name,
                "phone": obj.phone,
                "zipcode": obj.zipcode,
                "address": obj.address,
                "address_detail": obj.address_detail,
                "request": obj.request,
            }
        ).data


class OrderStatusPatchSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=OrderStatus.choices)


class OrderDeliveryNumberPatchSerializer(serializers.Serializer):
    tracking_number = serializers.CharField(allow_null=True)
