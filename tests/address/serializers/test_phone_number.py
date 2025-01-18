import pytest

from address.serializers import AddressSerializer
from address.exceptions import AddressException


def test_invalid_phone_num():
    serializer = AddressSerializer()
    with pytest.raises(Exception):
        serializer.validate_phone(value='qwer')



def test_valid_phone_num():
    serializer = AddressSerializer()
    assert serializer.validate_phone(value='01012341234') == '01012341234'