# Generated by Django 5.0 on 2023-12-25 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_payment_method_reverse_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment_method',
            name='reverse_url',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
