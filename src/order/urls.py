from django.urls import path

from .views.order import OrderView, OrderDetailView
from .views.pg import PGView
from .views.staging import OrderStagingView

urlpatterns = [
    path('', OrderView.as_view()),
    path('/<uuid:order_id>', OrderDetailView.as_view()),
    path('/staging', OrderStagingView.as_view()),
    path('/payment/success', PGView.as_view()),
    path('/payment/fail', PGView.as_view()),
]