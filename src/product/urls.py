from rest_framework import routers

from product.viewsets import ProductViewSet

product_router = routers.DefaultRouter(trailing_slash=False)

product_router.register("product", ProductViewSet, basename="product")
