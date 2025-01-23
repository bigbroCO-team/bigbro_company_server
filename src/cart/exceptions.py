from core.exceptions import BaseCustomException


class CartExceptions:
    cartNotFound = BaseCustomException(code=404, detail='Cart not found')
    countIsNotAvailable = BaseCustomException(code=400, detail='Count is not available')