from django.urls import path

from .views.delivery_num import OrderDeliveryNumberPatchView
from .views.order import OrderView, OrderDetailView, AllOrderView
from .views.order_status import OrderStatusPatchView
from .views.pg import PGView
from .views.staging import OrderStagingView

urlpatterns = [
    path('', OrderView.as_view()),
    path('/all', AllOrderView.as_view()),
    path('/<uuid:order_id>', OrderDetailView.as_view()),
    path('/staging', OrderStagingView.as_view()),
    path('/payment/success', PGView.as_view()),
    path('/status/<uuid:order_id>', OrderStatusPatchView.as_view()),
    path('/delivery/<uuid:order_id>', OrderDeliveryNumberPatchView.as_view()),
]