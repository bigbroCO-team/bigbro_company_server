from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from address.services.address import AddressService
from core.authentication import CsrfExemptSessionAuthentication
from address.exceptions import AddressNotFoundException
from address.models import Address
from address.serializers import AddressSerializer


class AddressView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        serializer = AddressSerializer(AddressService().get_my_address(request), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        AddressService().save(user=request.user, serializer=serializer)
        return Response(status=status.HTTP_201_CREATED)
    
    @transaction.atomic
    def put(self, request: Request, address_id: int) -> Response:
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        AddressService().update(user=request.user, address_id=address_id, serializer=serializer)
        return Response(status=status.HTTP_200_OK)
    
    @transaction.atomic
    def delete(self, request: Request, address_id: int) -> Response:
        AddressService().delete(user=request.user, address_id=address_id)
        return Response(status=status.HTTP_204_NO_CONTENT)