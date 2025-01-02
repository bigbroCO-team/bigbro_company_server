from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth import login, authenticate, logout
from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction
from accounts.exceptions import AccountException
from accounts.serializers import LoginSerializer, SignupSerializer


class LoginView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(description='로그인 성공'),
            400: OpenApiResponse(description='로그인 실패')
        },
        description='로그인 API',
    )
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, **serializer.validated_data)
        if not user:
            raise AccountException.LoginFailException
        login(request, user)
        return Response(status=status.HTTP_200_OK)


class SignupView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    @extend_schema(
        request=SignupSerializer,
        responses={
            200: OpenApiResponse(description='회원가입 성공'),
            400: OpenApiResponse(description='회원가입 실패')
        },
        description='회원가입 API',
    )
    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: OpenApiResponse(description='로그아웃 성공'),
            401: OpenApiResponse(description='로그아웃 실패')
        },
        description='로그아웃 API',
    )
    def post(self, request: Request) -> Response:
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
