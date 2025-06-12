from django.db import models


class OrderItemStatus(models.TextChoices):
    STAGING = 'STAGING'
    PURCHASED = 'PURCHASED'
    PREPARE_SHIP = 'PREPARING'
    START_SHIP = 'START_SHIP'
    IN_SHIP = 'IN_SHIP'
    DELIVERED = 'DELIVERED'
    COMPLETED = 'COMPLETED'