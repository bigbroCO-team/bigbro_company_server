from rest_framework.request import Request

from accounts.models import User


class MyInfoService:
    def get_my_info(self, request: Request):
        return User.objects.prefetch_related("address").get(id=request.user.id)
