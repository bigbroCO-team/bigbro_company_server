from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import patch


@patch('django.contrib.auth.login')
@patch('accounts.models.User.get_or_create')
@patch('requests.get')
@patch('requests.post')
def test_kakao_login_callback(
    request_post, 
    request_get, 
    user_get_or_create,
    login
    ):
    
    client = APIClient()
    url = reverse('auth-kakao-callback')
    
    request_post.return_value.status_code = 200
    request_post.return_value.json.return_value = {
        'access_token':'access_token'
    }

    request_get.return_value.status_code = 200
    request_get.return_value.json.return_value = {
        'kakao_account': {'email': 'email@email.com'}
    }

    user_get_or_create.return_value = True

    login.return_value = True

    response = client.get(url)

    assert response.status_code == 302
