from core.exceptions import BaseCustomException

class AddressException:
    addressNotFound = BaseCustomException(code=400, detail="Address Not Found.")
    phoneNumberIsNotValid = BaseCustomException(code=400, detail="Phone Number Is Not Valid.")