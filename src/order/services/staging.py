from order.exceptions import OrderNotFoundException
from order.models import Order


class OrderStagingService:
    def __init__(self, order: Order = Order):
        self.order = order
    def get(self):
        order = self.order.objects.order_by('-created_at').first()
        if not order:
            raise OrderNotFoundException()
        return order