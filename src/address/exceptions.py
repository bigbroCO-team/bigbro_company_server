from rest_framework import status
from rest_framework.exceptions import APIException


class AddressTooManyDefaultFieldException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "기본 배송지는 하나만 설정할 수 있습니다."
    default_code = "too_many_default_field"
