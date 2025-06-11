from django.db import models

from accounts.models import User
from product.models import Product, ProductOption


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    total_price = models.PositiveIntegerField(null=True)

    tracking_number = models.CharField(max_length=50, null=True, blank=True)
    delivery_company = models.CharField(max_length=50, null=True, blank=True)

    address = models.TextField()
    address_detail = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    request = models.TextField(null=True)
    phone = models.CharField(max_length=11)

    # TODO: PG사 결제 연동 시 필요한 필드
#   paymentkey = models.CharField()
#   orderid = models.CharField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        db_table = 'order'

    def __str__(self):
        return self.user.username
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_item")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_option = models.ForeignKey(ProductOption, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveSmallIntegerField()
    
    class Meta:
        db_table = 'order_item'