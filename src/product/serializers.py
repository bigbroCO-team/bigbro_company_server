from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from .models import Product, ProductOption, ProductImage


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
        return [o.name for o in obj.option.all()]

    def get_images(self, obj):
        return [i.url for i in obj.image.all()]



class ProductWriteSerializer(serializers.ModelSerializer):
    option = serializers.ListField(write_only=True)
    image = serializers.ListField(write_only=True)
    discount = serializers.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    class Meta:
        model = Product
        fields = ('id', 'brand', 'name', 'description', 'price', 'discount', 'status', 'created', 'option', 'image')