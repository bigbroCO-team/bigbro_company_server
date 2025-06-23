import base64

import requests

from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import APIException

from order.enums import OrderStatus
from order.exceptions import InvalidAmountException, AlreadyPaidException, InvalidOrderStatusException
from order.models import Order, OrderItem


class PaymentService:
    @staticmethod
    def get_encrypted_secret_key():
        key_string = settings.TOSS_SECRET_KEY + ":"
        key = base64.b64encode(key_string.encode('utf-8')).decode('utf-8')
        return f'Basic {key}'

    @transaction.atomic
    def process_payment(self, user, payment_key, order_id, amount):
        order = get_object_or_404(
            Order,
            id=order_id,
            user=user
        )

        if order.paymentkey:
            raise AlreadyPaidException()

        if not int(order.total_price) == int(amount):
            raise InvalidAmountException(
                f"total_price: {order.total_price}, amount: {amount} is not correct"
            )

        if not order.status == OrderStatus.STAGING:
            raise InvalidOrderStatusException()

        response = requests.post(
            url="https://api.tosspayments.com/v1/payments/confirm",
            headers={
                'Authorization': PaymentService.get_encrypted_secret_key(),
                'Content-Type': 'application/json'
            },
            data={
                'orderId': order_id,
                'amount': int(order.total_price),
                'paymentKey': payment_key,
            }
        )

        if response.status_code == 200:
            order.paymentkey = payment_key
            order.save()

            OrderItem.objects.filter(order=order).update(status=OrderStatus.PURCHASED)

        else:
            raise APIException(detail=response.json(), code=response.status_code)