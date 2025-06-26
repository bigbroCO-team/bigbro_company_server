from rest_framework import status
from rest_framework.exceptions import APIException


class OptionDoesNotBelongToProduct(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "해당 옵션은 선택된 상품에 속하지 않습니다."
    default_code = "option_does_not_belong_to_product"
