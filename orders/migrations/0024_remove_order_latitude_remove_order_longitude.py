# Generated by Django 5.0 on 2023-12-21 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0023_remove_order_delivery_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='order',
            name='longitude',
        ),
    ]
