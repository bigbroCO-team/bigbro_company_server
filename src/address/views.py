from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from core.authentication import CsrfExemptSessionAuthentication
from .exceptions import AddressNotFoundException
from .models import Address
from .serializers import AddressSerializer


class AddressView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        address = Address.objects.filter(user_id=request.user)
        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED)
    
    @transaction.atomic
    def put(self, request: Request, address_id: int) -> Response:
        address = Address.objects.filter(id=address_id, user=request.user).first()
        if not address:
            raise AddressNotFoundException()
        serializer =  AddressSerializer(address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    
    @transaction.atomic
    def delete(self, request: Request, address_id: int) -> Response:
        address = Address.objects.filter(id=address_id, user_id=request.user).first()
        if not address:
            raise AddressNotFoundException()
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)