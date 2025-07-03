from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from cart.models import Cart
from cart.serilaizers import CartReadSerializer, CartWriteSerializer
from core.authentication import CsrfExemptSessionAuthentication


class CartView(ViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = None

    def list(self, request: Request) -> Response:
        cart = Cart.objects.filter(user=request.user).select_related(
            "product", "option"
        )
        serializer = CartReadSerializer(cart, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request: Request) -> Response:
        serializer = CartWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Cart.add_count_or_create(user=request.user, data=serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)

    @transaction.atomic
    def destroy(self, request: Request, pk: int) -> Response:
        get_object_or_404(Cart, id=pk, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
