from django.db.models import QuerySet
from rest_framework import serializers

from .models import Product, ProductOption, ProductImage
from .exceptions import ProductException


class ProductReadSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()
    created = serializers.DateField(format='%Y-%m-%d', required=False)

    class Meta:
        model = Product
        fields = ('id', 'options', 'images', 'brand', 'name', 'description', 'price', 'discount', 'status', 'created')

    def get_options(self, product):
        return [i.name for i in product.options.all()]

    def get_images(self, product):
        return [i.url for i in product.images.all()]
    

class ProductWriteSerializer(serializers.ModelSerializer):
    images = serializers.ListField()
    options = serializers.ListField()
    created = serializers.DateField(format='%Y-%m-%d', required=False)

    class Meta:
        model = Product
        fields = ('id', 'options', 'images', 'brand', 'name', 'description', 'price', 'discount', 'status', 'created')

    def create(self, validated_data):
        options = validated_data.pop('options')
        images = validated_data.pop('images')

        product_obj = Product.objects.create(**validated_data)

        option_list = []
        for i in options:
            option_list.append(ProductOption(product=product_obj, name=i))
        ProductOption.objects.bulk_create(option_list)

        image_list = []
        for i in images:
            image_list.append(ProductImage(product=product_obj, url=i))
        ProductImage.objects.bulk_create(image_list)

        return validated_data
    
    def update(self, instance, validated_data):
        options = validated_data.pop('options')
        images = validated_data.pop('images')

        # Option 업데이트
        instance.options.all().delete()
        ProductOption.objects.bulk_create(
            ProductOption(product=instance, name=name) for name in options
        )

        # Image 업데이트
        instance.images.all().update()
        ProductImage.objects.bulk_create(
            ProductImage(product=instance, url=url) for url in images
        )

        Product.objects.update(**validated_data)

        return validated_data
    
    def validate_discount(self, value):
        if value < 0 or value > 100:
            raise ProductException.invalidDiscount
        return value