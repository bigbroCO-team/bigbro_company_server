from django.urls import path

from .views import KakaoLoginView, KakaoLoginCallBackView


urlpatterns = [
    path('/auth/kakao', 
        KakaoLoginView.as_view(), 
        name='auth-kakao'
    ),

    path('/auth/kakao/callback', 
        KakaoLoginCallBackView.as_view(), 
        name='auth-kakao-callback'
    )
]