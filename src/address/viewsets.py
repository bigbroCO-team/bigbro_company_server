from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from address.models import Address
from address.serializers import AddressSerializer
from core.authentication import CsrfExemptSessionAuthentication


class AddressViewSet(ViewSet):
    serializer_class = AddressSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request: Request) -> Response:
        addresses = Address.objects.filter(user=request.user)
        serializer = self.serializer_class(addresses, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, pk: int) -> Response:
        address = get_object_or_404(Address, id=pk, user=request.user)
        serializer = self.serializer_class(address)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request: Request, pk: int) -> Response:
        address = get_object_or_404(Address, id=pk, user=request.user)
        serializer = self.serializer_class(address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()

    @transaction.atomic
    def destroy(self, request: Request, pk: int) -> Response:
        address = get_object_or_404(Address, id=pk, user=request.user)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(url_path="default", methods=["get"], detail=False)
    def get_default(self, request: Request) -> Response:
        address = get_object_or_404(Address, user=request.user, default=True)
        serializer = self.serializer_class(address)
        return Response(serializer.data)

    @action(url_path="default/(?P<pk>\d+)", methods=["post"], detail=False)
    @transaction.atomic
    def set_default(self, request: Request, pk: int) -> Response:
        address = get_object_or_404(Address, id=pk, user=request.user)
        Address.objects.filter(user=request.user, default=True).update(default=False)
        address.default = True
        address.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
