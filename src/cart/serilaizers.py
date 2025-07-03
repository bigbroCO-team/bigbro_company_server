from django.core.validators import MinValueValidator
from rest_framework import serializers

from product.exceptions import ProductIsNotOnSaleException
from .exceptions import OptionDoesNotBelongToProduct
from .models import Cart
from product.models import ProductStatus, Product, ProductOption
from product.serializers import ProductOptionSerializer, ProductReadSerializer


class CartReadSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer()
    option = ProductOptionSerializer()

    class Meta:
        model = Cart
        fields = ("id", "product", "option", "count")


class CartWriteSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(status=ProductStatus.ON)
    )
    option = serializers.PrimaryKeyRelatedField(
        queryset=ProductOption.objects.filter(product__status=ProductStatus.ON)
    )

    count = serializers.IntegerField(
        validators=[MinValueValidator(1)],
    )

    class Meta:
        model = Cart
        fields = ("product", "option", "count")

    def validate(self, value):
        if not value.get("product").id == value.get("option").product.id:
            raise OptionDoesNotBelongToProduct()
        return value
