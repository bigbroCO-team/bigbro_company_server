from core.exceptions import BaseCustomException


class CartExceptions:
    cartNotFound = BaseCustomException(code=404, detail='Cart not found')