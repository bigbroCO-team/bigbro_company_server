from order.models import Order


class OrderStagingService:
    def __init__(self, order: Order = Order):
        self.order = order

    def get(self):
        return self.order.objects.filter(address__isnull=True)