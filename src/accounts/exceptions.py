from core.exceptions import BaseCustomException


class AccountException:
    LoginFailException = BaseCustomException(code=400, detail='Fail to login')
    UserNameAlreadyExistsException = BaseCustomException(code=400, detail='Username already exists')
    PasswordTooShortException = BaseCustomException(code=400, detail='Password must be at least 6 characters long')
