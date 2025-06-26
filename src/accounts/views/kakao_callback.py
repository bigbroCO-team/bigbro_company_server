from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.services.kakao_callback import KakaoLoginCallbackService
from core.authentication import CsrfExemptSessionAuthentication


class KakaoLoginCallBackView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = [AllowAny]

    kakao_login_callback_service = KakaoLoginCallbackService()

    def get(self, request: Request) -> Response:
        return Response(
            headers={"location": self.kakao_login_callback_service.login(request)},
            status=status.HTTP_302_FOUND,
        )
