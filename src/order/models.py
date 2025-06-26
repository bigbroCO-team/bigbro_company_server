import uuid

from django.db import models

from accounts.models import User
from core.basemodel import BaseModel
from order.enums import OrderStatus
from product.models import Product, ProductOption


class Order(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    total_price = models.PositiveIntegerField(null=True)  # 최종 총합 주문 가격

    # 배송 관련 info
    tracking_number = models.CharField(
        max_length=50, null=True, blank=True
    )  # 배송 추적 번호
    delivery_company = models.CharField(
        max_length=50, null=True, blank=True
    )  # 배송 회사명
    delivery_cost = models.PositiveIntegerField(default=3000)  # 배송비

    # 배송지 정보
    name = models.CharField(max_length=17)  # 수령인 이름
    phone = models.CharField(max_length=11)  # 수령인 연락처
    zipcode = models.CharField(max_length=10, null=True)  # 우편번호
    address = models.TextField(null=True)  # 주소지
    address_detail = models.CharField(max_length=50, null=True)  # 상세 주소
    request = models.TextField(null=True)  # 배송 요청사항
    phone = models.CharField(max_length=11, null=True)  # 연락처

    # 주문 상태
    status = models.CharField(
        choices=OrderStatus.choices, max_length=16, default=OrderStatus.STAGING
    )

    paymentkey = models.CharField(null=True, max_length=300)
    receipt_url = models.CharField(null=True, max_length=300)

    class Meta:
        db_table = "order"

    def __str__(self):
        return self.user.username


class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_item"
    )  # 주문
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=False
    )  # 상품
    product_option = models.ForeignKey(
        ProductOption, on_delete=models.SET_NULL, null=True, blank=False
    )  # 상품 옵션

    quantity = models.PositiveSmallIntegerField()  # 수량
    price = models.PositiveIntegerField(null=True, blank=False)  # 확정 가격

    class Meta:
        db_table = "order_item"
