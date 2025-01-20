from django.db import models


class ProductBrand(models.TextChoices):
    BIGBRO = 'BIGBRO'
    SCB = 'S.C.B'
    SCULFEE = 'SCULFEE'
    GONGNEWGI = 'GONGNEWGI'
    CBWAS = 'CBWAS'


class ProductStatus(models.TextChoices):
    ON = 'ON'
    OFF = 'OFF'
    EMPTY = 'EMPTY'


class Product(models.Model):
    brand = models.CharField(choices=ProductBrand.choices, max_length=9)
    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.PositiveIntegerField()
    discount = models.FloatField()
    status = models.CharField(choices=ProductStatus.choices, max_length=5)
    created = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    url = models.URLField()

    class Meta:
        db_table = 'product_image'

    def __str__(self):
        return self.product.name
    

class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'product_option'

    def __str__(self):
        return self.product.name