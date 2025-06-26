from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentication import CsrfExemptSessionAuthentication
from order.serializers import OrderReadSerializer
from order.services.staging import OrderStagingService


class OrderStagingView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    order_staging_service = OrderStagingService()

    def get(self, request):
        serializer = OrderReadSerializer(self.order_staging_service.get())
        return Response(serializer.data, status=status.HTTP_200_OK)
