# Generated by Django 5.1.5 on 2025-01-23 06:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0003_alter_cart_option_alter_cart_product"),
        ("product", "0003_alter_productimage_url"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="cart",
            unique_together={("user", "product", "option")},
        ),
    ]
