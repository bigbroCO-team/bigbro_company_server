from django.db import models

from accounts.models import User
from core.basemodel import BaseModel
from order.enums import OrderItemStatus
from product.models import Product, ProductOption


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    total_price = models.PositiveIntegerField(null=True)  # 최종 총합 주문 가격

    tracking_number = models.CharField(max_length=50, null=True, blank=True)  # 배송 추적 번호
    delivery_company = models.CharField(max_length=50, null=True, blank=True)  # 배송 회사명

    address = models.TextField()  # 주소지
    address_detail = models.CharField(max_length=50)  # 상세 주소
    zipcode = models.CharField(max_length=10)  # 우편번호
    request = models.TextField(null=True)  # 배송 요청사항
    phone = models.CharField(max_length=11)  # 연락처

    # TODO: PG사 결제 연동 시 필요한 필드
#   paymentkey = models.CharField()
#   orderid = models.CharField()

    class Meta:
        db_table = 'order'

    def __str__(self):
        return self.user.username
    

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_item")  # 주문
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=False)  # 상품
    product_option = models.ForeignKey(ProductOption, on_delete=models.SET_NULL, null=True, blank=False)  # 상품 옵션

    quantity = models.PositiveSmallIntegerField()  # 수량
    price = models.PositiveIntegerField(null=True, blank=False)  # 확정 가격

    # order item 상태
    status = models.CharField(
        choices=OrderItemStatus.choices,
        max_length=16,
        default=OrderItemStatus.STAGING
    )
    
    class Meta:
        db_table = 'order_item'