from django.urls import path

from address.views.address import AddressView


urlpatterns = [
    path('', AddressView.as_view()),
    path('/<int:address_id>', AddressView.as_view())
]