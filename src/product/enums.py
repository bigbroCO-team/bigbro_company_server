from django.db import models


class ProductBrand(models.TextChoices):
    BIGBRO = 'BIGBRO'
    SCB = 'S.C.B'
    SCULFEE = 'SCULFEE'
    GONGNEWGI = 'GONGNEWGI'
    CBWAS = 'CBWAS'


class ProductStatus(models.TextChoices):
    ON = 'ON'
    OFF = 'OFF'
    EMPTY = 'EMPTY'