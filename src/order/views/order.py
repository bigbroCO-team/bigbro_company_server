from uuid import UUID

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core.authentication import CsrfExemptSessionAuthentication
from order.serializers import (
    OrderReadSerializer,
    OrderWriteSerializer,
    OrderPatchSerializer,
)
from order.services.order import OrderService


class OrderView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = [IsAuthenticated]

    order_service = OrderService()

    def get(self, request: Request) -> Response:
        serializer = OrderReadSerializer(
            self.order_service.get_my_order_list(request.user), many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = OrderWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.order_service.create(user=request.user, serializer=serializer)
        return Response(status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = [IsAuthenticated]

    order_service = OrderService()

    def get(self, request: Request, order_id: UUID) -> Response:
        serializer = OrderReadSerializer(
            self.order_service.get_my_order_by_id(request.user, order_id)
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, order_id: UUID) -> Response:
        serializer = OrderPatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.order_service.patch(
            user=request.user, serializer=serializer, order_id=order_id
        )
        return Response(status=status.HTTP_200_OK)


class AllOrderView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = [IsAdminUser]

    order_service = OrderService()

    def get(self, request: Request) -> Response:
        serializer = OrderReadSerializer(
            self.order_service.get_all_order_list(), many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
