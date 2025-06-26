from rest_framework.routers import DefaultRouter

from address.viewsets import AddressViewSet


router = DefaultRouter(trailing_slash=False)

router.register("address", AddressViewSet, basename="address")
