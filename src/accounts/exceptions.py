from rest_framework.exceptions import APIException


class LoginFailException(APIException):
    status_code = 400
    default_detail = "Fail to login"
    default_code = "fail_to_login"
