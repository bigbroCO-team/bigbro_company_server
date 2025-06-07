from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.services.kakao_login import KakaoLoginService
from core.authentication import CsrfExemptSessionAuthentication


class KakaoLoginView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    kakao_login_service = KakaoLoginService()

    def get(self, request: Request) -> Response:
        return Response(headers={
            'Location': self.kakao_login_service.get_login_url(),
        }, status=status.HTTP_302_FOUND)

