# Generated by Django 5.0.6 on 2024-07-18 19:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_alter_customer_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 19, 0, 35, 0, 62608)),
        ),
    ]
