from django.contrib import admin
from django.urls import path, include
from address.urls import router as address_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(address_router.urls)),
    path("", include("accounts.urls")),
    path("", include("product.urls")),
    path("", include("cart.urls")),
    path("", include("order.urls")),
]
