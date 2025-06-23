from uuid import UUID

from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentication import CsrfExemptSessionAuthentication
from order.serializers import OrderDeliveryNumberPatchSerializer
from order.services.order import OrderService


class OrderDeliveryNumberPatchView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAdminUser, )

    order_service = OrderService()

    def patch(self, request: Request, order_id: UUID) -> Response:
        serializer = OrderDeliveryNumberPatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.order_service.patch_delivery_info(
            order_id=order_id,
            serializer=serializer
        )
        return Response(status=status.HTTP_200_OK)