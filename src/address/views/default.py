from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from address.serializers import AddressSerializer
from address.services.address import AddressService
from core.authentication import CsrfExemptSessionAuthentication


class DefaultAddressView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    address_service = AddressService()

    def get(self, request: Request) -> Response:
        return Response(AddressSerializer(
            self.address_service.get_default_address(request.user)).data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request, address_id: int) -> Response:
        self.address_service.set_default(user=request.user, address_id=address_id)
        return Response(status=status.HTTP_200_OK)