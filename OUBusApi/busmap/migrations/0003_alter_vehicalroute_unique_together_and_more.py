# Generated by Django 5.1.2 on 2024-10-29 03:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("busmap", "0002_alter_vehicleticket_is_pay"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="vehicalroute",
            unique_together={("route", "vehical", "driver")},
        ),
        migrations.AlterUniqueTogether(
            name="vehicleticket",
            unique_together={("register_trip", "vehical_route")},
        ),
    ]
