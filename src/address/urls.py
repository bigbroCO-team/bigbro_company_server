from rest_framework.routers import DefaultRouter

from address.viewsets import AddressViewSet


address_router = DefaultRouter(trailing_slash=False)

address_router.register("address", AddressViewSet, basename="address")
