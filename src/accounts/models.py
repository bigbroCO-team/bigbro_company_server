from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    password = models.CharField(null=True, max_length=256, blank=True)
    username = models.CharField(null=True, max_length=30, unique=True, blank=True)

    class Meta:
        db_table = 'user'

        verbose_name = 'User'

    @staticmethod
    def get_or_create(email: str):
        if not (user := User.objects.filter(email=email).first()):
            user = User.objects.create(email=email)
        return user

    def __str__(self):
        return self.email
