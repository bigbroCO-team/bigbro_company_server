from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.services.logout import LogoutService
from core.authentication import CsrfExemptSessionAuthentication


class LogoutView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request) -> Response:
        LogoutService().logout(request)
        return Response(status=status.HTTP_200_OK)
