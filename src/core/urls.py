from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account', include('accounts.urls'), name='account'),
    path('address', include('address.urls'), name='address'),
    path('product', include('product.urls'), name='product'),
    path('cart', include('cart.urls'), name='cart'),
]
