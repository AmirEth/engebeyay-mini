# Generated by Django 4.1.4 on 2023-05-31 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_remove_buyer_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryguy',
            name='status',
            field=models.CharField(default='Active', max_length=100),
        ),
    ]
