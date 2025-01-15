import requests

from django.conf import settings
from django.contrib.auth import login
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from core.authentication import CsrfExemptSessionAuthentication
from .exceptions import LoginException
from .models import User


class KakaoLoginView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        headers = {
            'Location': 
                f'https://kauth.kakao.com/oauth/authorize'
                f'?response_type=code'
                f'&client_id={settings.KAKAO_API_KEY}'
                f'&redirect_uri={settings.KAKAO_REDIRECT_URI}'
            }
        return Response(headers=headers, status=status.HTTP_302_FOUND)
    

class KakaoLoginCallBackView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        # Get access token 
        access_token_response = requests.post(
            url='https://kauth.kakao.com/oauth/token',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'grant_type': 'authorization_code',
                'client_id': settings.KAKAO_API_KEY,
                'redirect_uri': settings.KAKAO_REDIRECT_URI,
                'code': request.GET.get('code'),
            }
        )
        if not access_token_response.status_code == 200:
            raise LoginException.LoginFailException
        access_token = access_token_response.json().get('access_token')

        # Get userinfo
        user_info_response = requests.get(
            url="https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if not user_info_response.status_code == 200:
            raise LoginException.LoginFailException
        user_email = user_info_response.json()["kakao_account"]["email"]

        user = User.get_or_create(email=user_email)

        login(request, user)

        headers={'Location': settings.KAKAO_CLIENT_REDIRECT_URL}
        return Response(headers=headers, status=status.HTTP_302_FOUND)