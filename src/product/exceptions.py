from rest_framework.exceptions import APIException


class ProductIsNotOnSaleException(APIException):
    status_code = 400
    detail = "Product is not on sale"
    default_code = "productIsNotOnSaleException"


class InvalidDiscountException(APIException):
    status_code = 400
    detail = "Invalid Discount."
    default_code = "invalidDiscount"


class OptionNotFoundException(APIException):
    status_code = 404
    detail = "Option Not Found."
    default_code = "option_not_found"


class InvalidProductQueryException(APIException):
    status_code = 400
    detail = "Invalid Product Query."
    default_code = "invalid_product_query"


class ProductNotFoundException(APIException):
    status_code = 404
    detail = "Product Not Found."
    default_code = "product_not_found"
