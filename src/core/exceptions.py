from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class BaseCustomException(APIException): 
    def __init__(self, code, detail):
        self.status_code = code
        self.detail = detail

def custom_exception_handler(exception, context):
    response = exception_handler(exception, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    return response