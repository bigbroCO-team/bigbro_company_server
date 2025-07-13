from uuid import UUID

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from core.authentication import CsrfExemptSessionAuthentication
from order.enums import OrderStatus
from order.exceptions import OrderNotFoundException
from order.models import Order
from order.payment import process_payment
from order.serializers import (
    OrderReadSerializer,
    OrderWriteSerializer,
    OrderUpdateSerializer,
    OrderStatusPatchSerializer,
    OrderDeliveryNumberPatchSerializer,
)
from order.services import create_order


class OrderViewSet(ViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    # 자신의 order 조회
    def list(self, request: Request) -> Response:
        order = Order.objects.filter(user=request.user).prefetch_related("order_item")
        serializer = OrderReadSerializer(order, many=True)
        return Response(serializer.data)

    # id로 자신의 order 조회
    def retrieve(self, request: Request, order_id: UUID) -> Response:
        order = get_object_or_404(Order, id=order_id, user=request.user)
        serializer = OrderReadSerializer(order)
        return Response(serializer.data)

    # Staging인 자신의 order 조회
    @action(url_path="staging", methods=["get"], detail=False)
    def staging(self, request: Request) -> Response:
        order = Order.objects.order_by("-created_at").first()
        if not order:
            raise OrderNotFoundException()
        serializer = OrderReadSerializer(order)
        return Response(serializer.data)

    # Order 생성
    @transaction.atomic
    def create(self, request: Request) -> Response:
        serializer = OrderWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_order(user=request.user, serializer=serializer)
        return Response(status=status.HTTP_201_CREATED)

    # Staging Order에 Address field update
    @transaction.atomic
    def partial_update(self, request: Request, order_id: UUID) -> Response:
        order = get_object_or_404(Order, id=order_id, user=request.user)
        serializer = OrderUpdateSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # ===PG API===
    # 결제 승인
    @action(url_path="payment/success", methods=["get"], detail=False)
    @transaction.atomic
    def payment_success_callback(self, request: Request) -> HttpResponseRedirect:
        process_payment(
            user=request.user,
            payment_key=request.GET.get("paymentKey"),
            order_id=request.GET.get("orderId"),
            amount=request.GET.get("amount"),
        )
        return redirect("https://www.bigbro.company/success")

    # ===Admin API===
    # 모든 order 조회
    @action(
        url_path="all", methods=["get"], detail=False, permission_classes=(IsAdminUser,)
    )
    def all(self, request: Request) -> Response:
        order = Order.objects.filter(~Q(status=OrderStatus.STAGING)).prefetch_related(
            "order_item"
        )
        serializer = OrderReadSerializer(order, many=True)
        return Response(serializer.data)

    # order status 수정
    @action(
        url_path=r"status/(?P<pk>\w+)",
        methods=["get"],
        detail=False,
        permission_classes=(IsAdminUser,),
    )
    @transaction.atomic
    def update_order_status(self, request: Request, pk: UUID) -> Response:
        serializer = OrderStatusPatchSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        order = get_object_or_404(Order, id=pk)
        order.status = serializer.validated_data.get("status")
        order.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # 배송 추적 번호 수정
    @action(
        url_path=r"delivery/(?P<pk>\w+)",
        methods=["get"],
        detail=False,
        permission_classes=(IsAdminUser,),
    )
    @transaction.atomic
    def update_delivery_number(self, request: Request, pk: UUID) -> Response:
        serializer = OrderDeliveryNumberPatchSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        order = get_object_or_404(Order, id=pk)
        order.tracking_number = serializer.validated_data.get("tracking_number")
        order.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
