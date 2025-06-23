from rest_framework.exceptions import APIException


class OrderNotFoundException(APIException):
    status_code = 404
    default_detail = 'Order Not Found'
    default_code = 'order_not_found'


class InvalidAmountException(APIException):
    status_code = 400
    default_detail = 'Invalid Amount'
    default_code = 'invalid_amount'


class AlreadyPaidException(APIException):
    status_code = 400
    default_detail = 'Order Already Paid'
    default_code = 'order_already_paid'


class InvalidOrderStatusException(APIException):
    status_code = 400
    default_detail = 'Invalid Order Status'
    default_code = 'invalid_order_status'