# Generated by Django 4.1.4 on 2023-05-16 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_deliveryguy_company'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buyer',
            old_name='location',
            new_name='latitude',
        ),
        migrations.AddField(
            model_name='buyer',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
    ]
