from django.urls import reverse
from rest_framework.test import APIClient


def test_kakao_login_redirect():
    client = APIClient()
    url = reverse('auth-kakao')
    
    response = client.get(url)

    assert response.status_code == 302
