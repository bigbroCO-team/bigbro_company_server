from django.contrib import admin
from django.urls import path, include

from address.urls import address_router
from accounts.urls import account_router
from cart.urls import cart_router
from order.urls import order_router
from product.urls import product_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(address_router.urls)),
    path("", include(account_router.urls)),
    path("", include(cart_router.urls)),
    path("", include(order_router.urls)),
    path("", include(product_router.urls)),
]
