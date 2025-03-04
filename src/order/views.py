import pgtransaction
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from core.authentication import CsrfExemptSessionAuthentication
from .models import Order
from .serializers import OrderReadSerializer, OrderWriteSerializer


class OrderView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        order = Order.objects.filter(user=request.user)
        serializer = OrderReadSerializer(order, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    @pgtransaction.atomic(isolation_level=pgtransaction.SERIALIZABLE)
    def post(self, request: Request) -> Response:
        serializer = OrderWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(status=HTTP_201_CREATED)
    