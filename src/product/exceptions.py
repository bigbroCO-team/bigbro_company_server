from core.exceptions import BaseCustomException


class ProductException:
    invalidQueryException = BaseCustomException(code=400, detail='Invalid Query.')
    productNotFound = BaseCustomException(code=404, detail='Product Not Found.')
    invalidDiscount = BaseCustomException(code=400, detail='Invalid Discount.')
    optionNotFound = BaseCustomException(code=404, detail='Options Not Found.')
    productIsNotOnSale = BaseCustomException(code=400, detail='Product is not on sale')