from rest_framework.exceptions import APIException


class OrderNotFoundException(APIException):
    status_code = 404
    default_detail = 'Order Not Found'
    default_code = 'order_not_found'


class InvalidAmountException(APIException):
    status_code = 400
    default_detail = 'Invalid Amount'
    default_code = 'invalid_amount'
