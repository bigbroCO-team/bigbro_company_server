from django.core.validators import MinValueValidator
from rest_framework import serializers

from product.exceptions import ProductIsNotOnSaleException
from .models import Cart
from product.models import ProductStatus
from product.serializers import ProductOptionSerializer, ProductReadSerializer


class CartReadSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer()
    option = ProductOptionSerializer()

    class Meta:
        model = Cart
        fields = ('product', 'option', 'count')


class CartWriteSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(
        validators=[MinValueValidator(1)],
    )

    class Meta:
        model = Cart
        fields = ('product', 'option', 'count')
    
    def validate_product(self, value):
        if not value.status == ProductStatus.ON:
            raise ProductIsNotOnSaleException()
        return value