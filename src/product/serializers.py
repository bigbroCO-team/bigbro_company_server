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
    options = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'brand', 'name', 'description', 'price', 'discount', 'status', 'created', 'options', 'images')

    def get_options(self, obj):
        return [str(o) for o in obj.option.all()]

    def get_images(self, obj):
        return [str(i) for i in obj.option.all()]



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