# Generated by Django 5.0 on 2023-12-21 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0022_refund_is_payed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery_company',
        ),
    ]
