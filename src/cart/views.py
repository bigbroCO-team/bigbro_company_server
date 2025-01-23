from django.db import transaction
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from core.authentication import CsrfExemptSessionAuthentication
from .models import Cart
from .serilaizers import CartReadSerializer, CartWriteSerializer
from .exceptions import CartExceptions


class CartView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        cart = Cart.objects.filter(user=request.user).prefetch_related('product', 'option')
        serializer = CartReadSerializer(cart, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = CartWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(status=HTTP_200_OK)
    
    @transaction.atomic
    def delete(self, request: Request, cart_id: int) -> Response:
        cart = Cart.objects.filter(user=request.user, id=cart_id).first()
        if not cart:
            raise CartExceptions.cartNotFound
        cart.delete()
        return Response(status=HTTP_204_NO_CONTENT)