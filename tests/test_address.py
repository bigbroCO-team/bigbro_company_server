from unittest import TestCase

import pytest

from address.exceptions import PhoneNumberIsNotValidException
from address.serializers import AddressSerializer


class TestAddress(TestCase):
    def test_invalid_phone_num(self):
        serializer = AddressSerializer()
        with pytest.raises(PhoneNumberIsNotValidException):
            serializer.validate_phone(value='qwer')

    def test_valid_phone_num(self):
        serializer = AddressSerializer()
        assert serializer.validate_phone(value='01012341234') == '01012341234'