import pytest

from product.serializers import ProductWriteSerializer


def test_invalid_discount_under_zero():
    serializer = ProductWriteSerializer()

    with pytest.raises(Exception) as e:
        serializer.validate_discount(value=-1)


def test_invalid_discount_over_h():
    serializer = ProductWriteSerializer()

    with pytest.raises(Exception) as e:
        serializer.validate_discount(value=101)
