from django.db import models
from django.db.models import QuerySet

from core.basemodel import BaseModel
from product.enums import ProductBrand, ProductStatus


class Product(BaseModel):
    brand = models.CharField(choices=ProductBrand.choices, max_length=9)
    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.PositiveIntegerField()
    discount = models.FloatField()
    status = models.CharField(choices=ProductStatus.choices, max_length=5)

    image: "QuerySet[ProductImage]"
    option: "QuerySet[ProductOption]"

    class Meta:
        db_table = "product"

    def update_option(self, option):
        self.option.all().delete()
        ProductOption.objects.bulk_create(
            [ProductOption(product=self, name=name) for name in option],
        )

    def update_image(self, image):
        self.image.all().delete()
        ProductImage.objects.bulk_create(
            [ProductImage(product=self, url=url) for url in image],
        )


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="image")
    url = models.URLField(max_length=500)

    class Meta:
        db_table = "product_image"


class ProductOption(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="option"
    )
    name = models.CharField(max_length=30)

    class Meta:
        db_table = "product_option"
