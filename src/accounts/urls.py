from django.urls import path

from .views import KakaoLoginView, KakaoLoginCallBackView, LogoutView


urlpatterns = [
    path('/auth/logout', LogoutView.as_view()),

    path('/auth/kakao', KakaoLoginView.as_view(), name='auth-kakao'),
    path('/auth/kakao/callback', KakaoLoginCallBackView.as_view(), name='auth-kakao-callback')
]