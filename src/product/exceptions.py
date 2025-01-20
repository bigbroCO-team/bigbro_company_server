from core.exceptions import BaseCustomException


class ProductException:
    invalidQueryException = BaseCustomException(code=400, detail='Invalid Query.')
    ProductNotFound = BaseCustomException(code=404, detail='Product Not Found.')