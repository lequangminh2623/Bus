# Generated by Django 5.1.2 on 2024-10-29 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("busmap", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehicleticket",
            name="is_pay",
            field=models.BooleanField(default=False),
        ),
    ]
