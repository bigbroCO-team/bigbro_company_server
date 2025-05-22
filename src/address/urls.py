from django.urls import path

from address.views.address import AddressView
from address.views.default import DefaultAddressView

urlpatterns = [
    path('', AddressView.as_view()),
    path('/<int:address_id>', AddressView.as_view()),
    path('/default', DefaultAddressView.as_view()),
]