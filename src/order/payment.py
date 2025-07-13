import base64
from uuid import UUID

import requests
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import APIException

from accounts.models import User
from order.enums import OrderStatus
from order.models import Order


def process_payment(user: User, order_id: UUID, payment_key: str, amount: int):
    order = get_object_or_404(
        Order,
        ~Q(status=OrderStatus.STAGING),  # 주문 상태가 Staging이 아닌 경우
        id=order_id,
        user=user,
        paymentkey__isnull=True,  # 결제 키가 없는 주문만 처리
        total_price=amount,  # 가격 검증
    )

    receipt_url = _confirm_payment(
        order_id=order_id, total_price=amount, payment_key=payment_key
    )

    # Todo: Confirm 후 insert 실패시 롤백 로직 구현
    order.paymentkey = payment_key
    order.save()
    Order.objects.filter(id=order.id).update(
        status=OrderStatus.PURCHASED, receipt_url=receipt_url
    )


def _get_encrypted_pg_secret_key():
    key_string = settings.TOSS_SECRET_KEY or "" + ":"
    key = base64.b64encode(key_string.encode("utf-8")).decode("utf-8")
    return f"Basic {key}"


def _confirm_payment(order_id: UUID, total_price: int, payment_key: str) -> str:
    response = requests.post(
        url="https://api.tosspayments.com/v1/payments/confirm",
        headers={
            "Authorization": _get_encrypted_pg_secret_key(),
            "Content-Type": "application/json",
        },
        json={
            "orderId": order_id,
            "amount": total_price,
            "paymentKey": payment_key,
        },
    )

    if response.status_code != 200:
        raise APIException(detail=response.json(), code=response.status_code)

    return response.json().get("receipt").get("url")
