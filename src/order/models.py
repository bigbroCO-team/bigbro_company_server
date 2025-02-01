from django.db import models

from accounts.models import User
from product.models import Product, ProductOption


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    total_price = models.PositiveIntegerField(null=True)

    traking_number = models.CharField(max_length=50, null=True)
    delivery_company = models.CharField(max_length=50, null=True)

    address = models.TextField()
    address_detail = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    request = models.TextField(null=True)
    phone = models.CharField(max_length=11)

#   paymentkey = models.CharField()
#   orderid = models.CharField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        db_table = 'order'

    def __str__(self):
        return self.user.username
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_option = models.ForeignKey(ProductOption, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'order_item'