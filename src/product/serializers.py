from rest_framework import serializers

from .models import Product, ProductOption, ProductImage
from .exceptions import ProductException
    

class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = ('id', 'name')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'url')


class ProductReadSerializer(serializers.ModelSerializer):
    option = ProductOptionSerializer(many=True, read_only=True)
    image = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'brand', 'name', 'description', 'price', 'discount', 'status', 'created', 'option', 'image')


class ProductWriteSerializer(serializers.ModelSerializer):
    option = serializers.ListField(write_only=True)
    image = serializers.ListField(write_only=True)

    class Meta:
        model = Product
        fields = ('id', 'brand', 'name', 'description', 'price', 'discount', 'status', 'created', 'option', 'image')

    def validate_discount(self, value):
        if value < 0 or value > 100:
            raise ProductException.invalidDiscount
        return value