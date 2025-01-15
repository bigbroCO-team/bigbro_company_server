from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    class Meta:
        db_table = 'user'

        verbose_name = 'User'

    @staticmethod
    def get_or_create(email: str):
        if not (user := User.objects.filter(email=email).first()):
            user = User.objects.create(email=email)
        return user

    def __str__(self):
        return self.username
