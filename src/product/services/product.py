from django.db import transaction
from django.shortcuts import get_object_or_404

from product.enums import ProductStatus
from product.exceptions import InvalidProductQueryException
from product.models import Product, ProductOption, ProductImage
from product.serializers import ProductWriteSerializer


class ProductService:
    def get_on_product_list(self, brand_name: str = None):
        if brand_name:
            return Product.objects.filter(
                brand=brand_name, status=ProductStatus.ON
            ).prefetch_related("image", "option")
        else:
            return Product.objects.filter(
                status=ProductStatus.ON
            ).prefetch_related("image", "option")

    def get_all_product_list(self, brand_name: str = None):
        if brand_name:
            return Product.objects.filter(brand=brand_name).prefetch_related(
                "image", "option"
            )
        else:
            return Product.objects.all().prefetch_related("image", "option")

    def get_product_by_id(self, product_id: int = None):
        return (
            Product.objects.filter(id=product_id)
            .prefetch_related("image", "option")
            .first()
        )

    @transaction.atomic
    def save(self, serializer: ProductWriteSerializer):
        option = serializer.validated_data.pop("option")
        image = serializer.validated_data.pop("image")

        # Product 생성
        product = Product.objects.create(**serializer.validated_data)

        # Product option 생성
        option_list = []
        for i in option:
            option_list.append(ProductOption(product=product, name=i))
        ProductOption.objects.bulk_create(option_list)

        # Product image 생성
        image_list = []
        for i in image:
            image_list.append(ProductImage(product=product, url=i))
        ProductImage.objects.bulk_create(image_list)

    @transaction.atomic
    def update(self, product_id: int, serializer: ProductWriteSerializer):
        product = Product.objects.prefetch_related("option", "image").get(id=product_id)
        option = serializer.validated_data.pop("options")
        image = serializer.validated_data.pop("images")

        # Option 업데이트
        Product.option.all().delete()
        ProductOption.objects.bulk_create(
            [ProductOption(product=product, name=name) for name in option],
        )

        # Image 업데이트
        Product.image.all().delete()
        ProductImage.objects.bulk_create(
            [ProductImage(product=product, url=url) for url in image],
        )

        serializer.instance = product
        serializer.save()

    @transaction.atomic
    def delete(self, product_id: int):
        get_object_or_404(Product, id=product_id).delete()
