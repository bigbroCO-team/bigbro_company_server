from order.exceptions import OrderNotFoundException
from order.models import Order


class OrderStagingService:
    def get(self):
        order = Order.objects.order_by("-created_at").first()
        if not order:
            raise OrderNotFoundException()
        return order
