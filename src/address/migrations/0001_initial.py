# Generated by Django 5.1.5 on 2025-01-18 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.IntegerField()),
                ("name", models.CharField(max_length=17)),
                ("phone", models.CharField(max_length=11)),
                ("tag", models.CharField(max_length=20)),
                ("zipcode", models.CharField(max_length=10)),
                ("address", models.TextField()),
                ("detail", models.CharField(max_length=50)),
                ("request", models.TextField()),
            ],
            options={
                "db_table": "address",
            },
        ),
    ]
