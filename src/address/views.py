from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from core.authentication import CsrfExemptSessionAuthentication
from .models import Address
from .serializers import AddressSerializer
from .exceptions import AddressException


class AddressView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        address = Address.objects.filter(user_id=request.user.id)
        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user.id)
        return Response(status=HTTP_201_CREATED)
    
    @transaction.atomic
    def put(self, request: Request, address_id: int) -> Response:
        address = Address.objects.filter(id=address_id, user_id=request.user.id).first()
        if not address:
            raise AddressException.addressNotFound
        serializer =  AddressSerializer(address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_200_OK)
    
    @transaction.atomic
    def delete(self, request: Request, address_id: int) -> Response:
        address = Address.objects.filter(id=address_id, user_id=request.user.id).first()
        if not address:
            raise AddressException.addressNotFound
        address.delete()
        return Response(status=HTTP_204_NO_CONTENT)