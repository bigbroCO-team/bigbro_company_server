from django.urls import path

from address.views.address import AddressView, AddressDetailView
from address.views.default import DefaultAddressView

urlpatterns = [
    path("", AddressView.as_view()),
    path("/<int:address_id>", AddressDetailView.as_view()),
    path("/default", DefaultAddressView.as_view()),
    path("/default/<int:address_id>", DefaultAddressView.as_view()),
]
