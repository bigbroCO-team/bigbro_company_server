from django.db import models
from django.contrib.auth.models import AbstractUser

from core.basemodel import BaseModel


class User(BaseModel, AbstractUser):
    password = models.CharField(null=True, max_length=256, blank=True)
    username = models.CharField(null=True, max_length=30, unique=True, blank=True)

    class Meta:
        db_table = "user"
        verbose_name = "User"

    def __str__(self):
        return self.email
