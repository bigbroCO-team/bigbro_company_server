from rest_framework.request import Request

from accounts.models import User


class MyInfoService:
    def __init__(self, user: User = User):
        self.user = user

    def get_my_info(self, request: Request):
        return self.user.objects.prefetch_related('address').get(id=request.user.id)
