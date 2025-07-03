from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from core.authentication import CsrfExemptSessionAuthentication, IsAdminOrReadOnly
from product.enums import ProductStatus
from product.models import Product, ProductOption, ProductImage
from product.serializers import ProductReadSerializer, ProductWriteSerializer


class ProductViewSet(ViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAdminOrReadOnly,)

    def list(self, request: Request) -> Response:
        brand = request.GET.get("brand")
        queryset = Product.objects.all().prefetch_related("image", "option")
        if brand:  # Brand filtering
            queryset = queryset.filter(brand=brand)
        products = (
            queryset
            if request.user.is_staff
            else queryset.filter(status=ProductStatus.ON)
        )
        serializer = ProductReadSerializer(products, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, pk: int) -> Response:
        product = get_object_or_404(
            Product.objects.prefetch_related("image", "option"), id=pk
        )
        serializer = ProductWriteSerializer(product)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request: Request) -> Response:
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
        get_object_or_404(Product, id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
