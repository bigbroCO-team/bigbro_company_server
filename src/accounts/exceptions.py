from core.exceptions import BaseCustomException


class LoginException:
    LoginFailException = BaseCustomException(code=400, detail='Fail to login')