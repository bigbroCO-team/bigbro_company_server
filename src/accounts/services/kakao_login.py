from django.conf import settings


class KakaoLoginService:
    def get_login_url(self):
        return (
            f"https://kauth.kakao.com/oauth/authorize"
            f"?response_type=code"
            f"&client_id={settings.KAKAO_API_KEY}"
            f"&redirect_uri={settings.KAKAO_REDIRECT_URI}"
        )
