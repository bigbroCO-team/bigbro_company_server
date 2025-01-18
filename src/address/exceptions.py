from core.exceptions import BaseCustomException

class AddressException:
    addressNotFound = BaseCustomException(code=400, detail="Address Not Found.")