from rest_framework import routers

from order.viewsets import OrderViewSet

order_router = routers.DefaultRouter(trailing_slash=False)

order_router.register("order", OrderViewSet, basename="order")
