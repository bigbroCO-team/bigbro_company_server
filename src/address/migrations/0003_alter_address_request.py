# Generated by Django 5.1.5 on 2025-01-18 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("address", "0002_alter_address_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="request",
            field=models.TextField(null=True),
        ),
    ]
