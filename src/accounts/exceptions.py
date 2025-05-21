from rest_framework.exceptions import APIException


class LoginFailException(APIException):
    status_code = 400
    default_detail = 'Fail to login'
    default_code = 'fail_to_login'


class UserNameAlreadyExistsException(APIException):
    status_code = 400
    default_detail = 'Username already exists'
    default_code = 'username_already_exists'


class PasswordTooShortException(APIException):
    status_code = 400
    default_detail = 'Password too short'
    default_code = 'password_too_short'
