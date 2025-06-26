from rest_framework.exceptions import APIException


class AddressNotFoundException(APIException):
    status_code = 404
    default_detail = "Address Not Found"
    default_code = "address_not_found"


class AddressTooManyDefaultFieldException(APIException):
    status_code = 400
    default_detail = "Address Can Have Only 1 Default Field"
    default_code = "address_can_have_only_one_default_field"


class DefaultAddressIsNotDeleteAble(APIException):
    status_code = 400
    default_detail = "Default Address Is Not Deleteable"
    default_code = "default_address_is_not_deleteable"
