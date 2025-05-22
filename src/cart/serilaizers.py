from rest_framework import serializers

from .models import Cart
from product.models import ProductStatus
from product.serializers import ProductOptionSerializer, ProductReadSerializer
from product.exceptions import ProductException
from .exceptions import CartExceptions


class CartReadSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer()
    option = ProductOptionSerializer()

    class Meta:
        model = Cart
        fields = '__all__'

        extra_kwargs = {
            'user': {'required': False, 'write_only': True}
        }


class CartWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('product', 'option', 'count')

    # count가 1 이상인지 검증
    def validate_count(self, value):
        if value < 1:
            raise CartExceptions.countIsNotAvailable
        return value
    
    # product가 판매중인지 검증
    def validate_product(self, value):
        if not value.status == ProductStatus.ON:
            raise ProductException.productIsNotOnSale
        return value