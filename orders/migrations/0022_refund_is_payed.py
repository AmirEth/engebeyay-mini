# Generated by Django 4.1.4 on 2023-06-10 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0021_orderedproduct_seller_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='refund',
            name='is_payed',
            field=models.BooleanField(default=False),
        ),
    ]
