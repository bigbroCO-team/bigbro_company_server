from django.db import models

from core.basemodel import BaseModel
from product.enums import ProductBrand, ProductStatus


class Product(BaseModel):
    brand = models.CharField(choices=ProductBrand.choices, max_length=9)
    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.PositiveIntegerField()
    discount = models.FloatField()
    status = models.CharField(choices=ProductStatus.choices, max_length=5)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.name
    

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image')
    url = models.URLField()

    class Meta:
        db_table = 'product_image'

    def __str__(self):
        return self.product.name
    

class ProductOption(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='option')
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'product_option'

    def __str__(self):
        return self.product.name