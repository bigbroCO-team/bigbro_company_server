from django.contrib import admin

from .models import Product, ProductOption, ProductImage


admin.site.register(Product)
admin.site.register(ProductOption)
admin.site.register(ProductImage)