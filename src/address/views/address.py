from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from address.services.address import AddressService
from address.serializers import AddressSerializer
from core.authentication import CsrfExemptSessionAuthentication


class AddressView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = [IsAuthenticated]

    address_service = AddressService()

    def get(self, request: Request) -> Response:
        return Response(
            AddressSerializer(
                self.address_service.get_my_address(user=request.user), many=True
            ).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request) -> Response:
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.address_service.save(user=request.user, serializer=serializer)
        return Response(status=status.HTTP_201_CREATED)


class AddressDetailView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = [IsAuthenticated]

    address_service = AddressService()

    def get(self, request: Request, address_id: int) -> Response:
        return Response(
            AddressSerializer(
                self.address_service.get_address_by_id(
                    user=request.user, address_id=address_id
                )
            ).data,
            status=status.HTTP_200_OK,
        )

    def put(self, request: Request, address_id: int) -> Response:
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.address_service.update(
            user=request.user, address_id=address_id, serializer=serializer
        )
        return Response(status=status.HTTP_200_OK)

    def delete(self, request: Request, address_id: int) -> Response:
        self.address_service.delete(user=request.user, address_id=address_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
