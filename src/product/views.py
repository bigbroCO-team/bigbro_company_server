from django.db import transaction
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from core.authentication import CsrfExemptSessionAuthentication, IsStaffOrReadOnly
from .models import Product
from .serializers import ProductReadSerializer, ProductWriteSerializer
from .exceptions import ProductException


class ProductView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsStaffOrReadOnly]
    
    def get(self, request: Request, product_id: int = None) -> Response:
        brand = request.GET.get('brand')
        if product_id:
            product = Product.objects.filter(id=product_id).prefetch_related('images', 'options').first()
            serializer = ProductReadSerializer(product)
        elif brand:
            product = Product.objects.filter(brand=brand).prefetch_related('images', 'options')
            serializer = ProductReadSerializer(product, many=True)
        else:
            raise ProductException.invalidQueryException

        return Response(serializer.data, status=HTTP_200_OK)
    
    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = ProductWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_201_CREATED)
    
    @transaction.atomic
    def put(self, request: Request, product_id: int) -> Response:
        product = Product.objects.filter(id=product_id).prefetch_related('images', 'options').first()
        if not product:
            raise ProductException.productNotFound
        serializer = ProductWriteSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_200_OK)
    
    @transaction.atomic
    def delete(self, request: Request, product_id: int) -> Response:
        product = Product.objects.filter(id=product_id).first()
        if not product:
            raise ProductException.productNotFound
        product.delete()
        return Response(status=HTTP_204_NO_CONTENT)
