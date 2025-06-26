from django.contrib.auth import logout
from rest_framework.request import Request


class LogoutService:
    def logout(self, request: Request) -> None:
        logout(request)
