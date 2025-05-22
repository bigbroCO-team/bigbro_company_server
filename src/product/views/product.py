from django.db import transaction
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from core.authentication import CsrfExemptSessionAuthentication, IsStaffOrReadOnly
from product.serializers import ProductReadSerializer, ProductWriteSerializer
from product.services.product import ProductService


class ProductView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsStaffOrReadOnly]
    
    def get(self, request: Request, product_id: int = None) -> Response:
        serializer = ProductReadSerializer(
            ProductService().get_product_list(
                product_id=product_id,
                brand_name=request.GET.get('brand'),
            ),
            many=True
        )
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request: Request) -> Response:
        serializer = ProductWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ProductService().save(serializer)
        return Response(status=HTTP_201_CREATED)
    
    def put(self, request: Request, product_id: int) -> Response:
        serializer = ProductWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ProductService().update(product=product_id, serializer=serializer)
        return Response(status=HTTP_200_OK)
    
    def delete(self, request: Request, product_id: int) -> Response:
        ProductService().delete(product_id=product_id)
        return Response(status=HTTP_204_NO_CONTENT)
