# Generated by Django 4.1.4 on 2023-05-31 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_rename_username_seller_merchant_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deliverycompany',
            old_name='first_name',
            new_name='company_name',
        ),
        migrations.RemoveField(
            model_name='deliverycompany',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='deliverycompany',
            name='username',
        ),
        migrations.RemoveField(
            model_name='deliveryguy',
            name='username',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='profile_image',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='username',
        ),
        migrations.AddField(
            model_name='deliverycompany',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='deliverycompany',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='seller',
            name='verification_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile/seller/'),
        ),
    ]
