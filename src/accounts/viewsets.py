from django.conf import settings
from django.contrib.auth import logout, login
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from accounts.kakao import kakao_login
from accounts.models import User
from accounts.serializers import MyInfoSerializer
from core.authentication import CsrfExemptSessionAuthentication


class AccountViewSet(ViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(url_path="my", methods=["get"], detail=False)
    def my(self, request: Request) -> Response:
        info = User.objects.prefetch_related("address").get(id=request.user.id)
        serializer = MyInfoSerializer(info)
        return Response(serializer.data)

    @action(url_path="auth/logout", methods=["delete"], detail=False)
    def logout(self, request: Request) -> Response:
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        url_path="auth/kakao",
        methods=["get"],
        detail=False,
        permission_classes=(AllowAny,),
    )
    def kakao_login(self, request: Request) -> HttpResponseRedirect:
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize"
            f"?response_type=code"
            f"&client_id={settings.KAKAO_API_KEY}"
            f"&redirect_uri={settings.KAKAO_REDIRECT_URI}"
        )

    @action(
        url_path="auth/kakao/callback",
        methods=["get"],
        detail=False,
        permission_classes=(AllowAny,),
    )
    @transaction.atomic
    def kakao_callback(self, request: Request) -> HttpResponseRedirect:
        user = kakao_login(request.GET.get("code"))
        login(request, user)
        return redirect(settings.KAKAO_CLIENT_REDIRECT_URL)
