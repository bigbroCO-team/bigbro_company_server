import requests
from django.conf import settings

from accounts.exceptions import LoginFailException
from accounts.models import User


def kakao_login(code) -> User:

    access_token = _fetch_kakao_access_token(code=code)

    email = _fetch_kakao_user_email(access_token=access_token)

    user, _ = User.objects.get_or_create(email=email)

    return user


def _fetch_kakao_access_token(code: str) -> str:
    access_token_response = requests.post(
        url="https://kauth.kakao.com/oauth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "authorization_code",
            "client_id": settings.KAKAO_API_KEY,
            "redirect_uri": settings.KAKAO_REDIRECT_URI,
            "code": code,
            "client_secret": settings.KAKAO_CLIENT_SECRET,
        },
    )
    if not access_token_response.status_code == 200:
        raise LoginFailException()

    return access_token_response.json().get("access_token")


def _fetch_kakao_user_email(access_token: str) -> str:
    user_info_response = requests.get(
        url="https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    if not user_info_response.status_code == 200:
        raise LoginFailException()

    return user_info_response.json().get("kakao_account").get("email")
