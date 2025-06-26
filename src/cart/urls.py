from rest_framework.routers import DefaultRouter

from cart.viewsets import CartView

cart_router = DefaultRouter(trailing_slash=False)

cart_router.register("cart", CartView, basename="cart")
