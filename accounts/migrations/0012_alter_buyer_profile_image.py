# Generated by Django 4.1.6 on 2023-03-20 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_buyer_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='profile_image',
            field=models.ImageField(blank=True, default='QR.png', null=True, upload_to=''),
        ),
    ]
