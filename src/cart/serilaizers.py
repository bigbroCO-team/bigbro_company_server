from rest_framework import serializers

from .models import Cart
from product.models import ProductOption, ProductStatus
from product.serializers import ProductReadSerializer, ProductOptionSerializer
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
    option = serializers.CharField()

    class Meta:
        model = Cart
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False, 'write_only': True}
        }

    # 기존 cart에 product가 있다면 count 증가, 없다면 생성
    def create(self, validated_data):
        option_data = validated_data.pop('option')

        # 이름으로 option 검색
        option_obj = ProductOption.objects.filter(
            product=validated_data['product'],
            name=option_data
        ).first()
        if not option_obj:
            raise ProductException.optionNotFound

        # 기존 Cart 조회
        cart = Cart.objects.filter(
            user=validated_data['user'], 
            product=validated_data['product'], 
            option=option_obj
        ).first()
        # 기존 cart가 있다면
        if cart:
            cart.count += validated_data['count']
            cart.save()
            return cart
        
        return Cart.objects.create(**validated_data, option=option_obj)

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