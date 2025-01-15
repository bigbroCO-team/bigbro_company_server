from unittest.mock import patch

from accounts.models import User


@patch('accounts.models.User.objects.filter')
def test_get_or_create_get(filter):
    filter.return_value.first.return_value = 'test'

    assert User.get_or_create(email='test'), 'test'


@patch('accounts.models.User.objects.filter')
@patch('accounts.models.User.objects.create')
def test_get_or_create_create(create, filter):
    filter.return_value.first.return_value = None

    create.return_value = 'test'

    result = User.get_or_create(email='test')
    assert result == 'test'
