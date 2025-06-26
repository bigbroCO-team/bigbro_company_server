from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_204_NO_CONTENT

from cart.services.cart import CartService
from cart.serilaizers import CartReadSerializer, CartWriteSerializer
from core.authentication import CsrfExemptSessionAuthentication


class CartView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = [IsAuthenticated]

    cart_service = CartService()

    def get(self, request: Request) -> Response:
        return Response(
            CartReadSerializer(
                self.cart_service.get_my_cart_list(user=request.user), many=True
            ).data,
            status=status.HTTP_200_OK,
        )

    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = CartWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.cart_service.save(user=request.user, serializer=serializer)
        return Response(status=status.HTTP_201_CREATED)

    @transaction.atomic
    def delete(self, request: Request, cart_id: int) -> Response:
        self.cart_service.delete(user=request.user, cart_id=cart_id)
        return Response(status=HTTP_204_NO_CONTENT)
