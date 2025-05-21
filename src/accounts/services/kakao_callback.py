import requests
from django.conf import settings
from django.contrib.auth import login
from django.db import transaction
from rest_framework.request import Request

from accounts.exceptions import LoginFailException
from accounts.models import User


class KakaoLoginCallbackService:
    @transaction.atomic
    def login(self, request: Request) -> str:
        access_token_response = requests.post(
            url='https://kauth.kakao.com/oauth/token',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'grant_type': 'authorization_code',
                'client_id': settings.KAKAO_API_KEY,
                'redirect_uri': settings.KAKAO_REDIRECT_URI,
                'code': request.GET.get('code'),
                'client_secret': settings.KAKAO_CLIENT_SECRET
            }
        )
        if not access_token_response.status_code == 200:
            raise LoginFailException()

        access_token = access_token_response.json().get('access_token')

        # Get userinfo
        user_info_response = requests.get(
            url="https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if not user_info_response.status_code == 200:
            raise LoginFailException()

        user_email = user_info_response.json()["kakao_account"]["email"]

        user = User.get_or_create(email=user_email)

        login(request, user)

        return settings.KAKAO_CLIENT_REDIRECT_URL