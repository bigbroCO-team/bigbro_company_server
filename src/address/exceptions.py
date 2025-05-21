from rest_framework.exceptions import APIException


class AddressNotFoundException(APIException):
    status_code = 404
    default_detail = 'Address Not Found'
    default_code = 'address_not_found'


class PhoneNumberIsNotValidException(APIException):
    status_code = 400
    default_detail = 'Phone Number Is Not Valid'
    default_code = 'phone_number_is_not_valid'


class AddressTooManyDefaultFieldException(APIException):
    status_code = 400
    default_detail = 'Address Can Have Only 1 Default Field'
    default_code = 'address_can_have_only_one_default_field'