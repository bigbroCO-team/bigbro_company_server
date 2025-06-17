from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.services.logout import LogoutService


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    logout_service = LogoutService()

    def delete(self, request: Request) -> Response:
        self.logout_service.logout(request)
        return Response(status=status.HTTP_200_OK)
