from rest_framework.exceptions import APIException

from core.exceptions import BaseCustomException


class ProductException:
    productNotFound = BaseCustomException(code=404, detail='Product Not Found.')
    invalidDiscount = BaseCustomException(code=400, detail='Invalid Discount.')
    optionNotFound = BaseCustomException(code=404, detail='Options Not Found.')
    productIsNotOnSale = BaseCustomException(code=400, detail='Product is not on sale')


class ProductOptionException:
    optionNotFound = BaseCustomException(code=404, detail='Option Not Found.')


class InvalidProductQueryException(APIException):
    status_code = 400
    detail = 'Invalid Product Query.'
    default_code = 'invalid_product_query'
