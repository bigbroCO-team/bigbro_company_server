from django.urls import path

from .views.kakao_callback import KakaoLoginCallBackView
from .views.kakao_login import KakaoLoginView
from .views.logout import LogoutView
from .views.my import MyInfoView


urlpatterns = [
    path('/auth/kakao', KakaoLoginView.as_view(), name='auth-kakao'),
    path('/auth/kakao/callback', KakaoLoginCallBackView.as_view(), name='auth-kakao-callback'),
    path('/auth/logout', LogoutView.as_view()),
    path('/my', MyInfoView.as_view()),
]