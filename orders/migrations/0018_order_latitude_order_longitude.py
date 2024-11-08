# Generated by Django 4.1.4 on 2023-05-16 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_order_is_qr_emailed'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
    ]
