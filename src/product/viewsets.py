from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from core.authentication import CsrfExemptSessionAuthentication, IsAdminOrReadOnly
from core.cache.mixin import CoreCacheMixin
from product.enums import ProductStatus
from product.models import Product, ProductOption, ProductImage
from product.serializers import ProductReadSerializer, ProductWriteSerializer


class ProductViewSet(ViewSet, CoreCacheMixin):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAdminOrReadOnly,)

    CACHE_KEY_PREFIX = "product"
    CACHE_TTL = 60 * 5

    def list(self, request: Request) -> Response:
        brand = request.GET.get("brand")
        return Response(
            self._cache_get_or_set(
                key=f"list::{brand or 'all'}::{request.user.is_staff}",
                value=lambda: ProductReadSerializer(
                    self._get_product_list(brand, is_staff=request.user.is_staff),
                    many=True,
                ).data,
            )
        )

    def retrieve(self, request: Request, pk: int) -> Response:
        return Response(
            self._cache_get_or_set(
                key=f"detail::{pk}::{request.user.is_staff}",
                value=lambda: ProductReadSerializer(
                    self._get_product_detail(pk, is_staff=request.user.is_staff)
                ).data,
            )
        )

    @transaction.atomic
    def create(self, request: Request) -> Response:
        self._cache_destroy_prefix_wild()
        serializer = ProductWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        option = serializer.validated_data.pop("option")
        image = serializer.validated_data.pop("image")
        product = Product.objects.create(**serializer.validated_data)
        ProductOption.objects.bulk_create(
            ProductOption(product=product, name=i) for i in option
        )
        ProductImage.objects.bulk_create(
            ProductImage(product=product, url=i) for i in image
        )
        return Response(status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request: Request, pk: int) -> Response:
        self._cache_destroy_prefix_wild()
        product = get_object_or_404(
            Product.objects.prefetch_related("option", "image"), id=pk
        )
        serializer = ProductWriteSerializer(data=request.data, instance=product)
        serializer.is_valid(raise_exception=True)
        product.update_option(option=serializer.validated_data.pop("option"))
        product.update_image(image=serializer.validated_data.pop("image"))
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def destroy(self, request: Request, pk: int) -> Response:
        self._cache_destroy_prefix_wild()
        get_object_or_404(Product, id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def _get_product_list(brand: str, is_staff: bool):
        queryset = Product.objects.all().prefetch_related("image", "option")
        if brand:
            queryset = queryset.filter(brand=brand)
        return queryset if is_staff else queryset.filter(status=ProductStatus.ON)

    @staticmethod
    def _get_product_detail(pk: int, is_staff: bool):
        queryset = Product.objects.prefetch_related("image", "option")
        if not is_staff:
            queryset = queryset.filter(status=ProductStatus.ON)
        return get_object_or_404(queryset, id=pk)
