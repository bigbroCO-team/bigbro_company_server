from django.urls import path

from .views.order import OrderView, OrderDetailView
from .views.staging import OrderStagingView

urlpatterns = [
    path('', OrderView.as_view()),
    path('/<int:order_id>', OrderDetailView.as_view()),
    path('/staging', OrderStagingView.as_view())
]