from rest_framework.routers import DefaultRouter

from accounts.viewsets import AccountViewSet

account_router = DefaultRouter(trailing_slash=False)

account_router.register("account", AccountViewSet, basename="account")
