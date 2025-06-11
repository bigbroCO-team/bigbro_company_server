from django.db import models


class OrderItemStatus(models.TextChoices):
    PURCHASED = 'PURCHASED'
    PREPARE_SHIP = 'PREPARING'
    START_SHIP = 'SHIPPING_STARTED'
    IN_SHIP = 'IN_SHIPPING'
    DELIVERED = 'DELIVERED'
    COMPLETED = 'COMPLETED'