# Generated by Django 5.1.5 on 2025-01-19 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_user_password_alter_user_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
    ]
