import pytest
from product.serializers import ProductWriteSerializer


def test_invalid_discount_str():
    serializer = ProductWriteSerializer()

    with pytest.raises(Exception):
        serializer.validate_discount(value='ff')

def test_invalid_discount_under_zero():
    serializer = ProductWriteSerializer()

    with pytest.raises(Exception):
        serializer.validate_phone(value=-1)

def test_invalid_discount_over_h():
    serializer = ProductWriteSerializer()

    with pytest.raises(Exception):
        serializer.validate_phone(value=101)