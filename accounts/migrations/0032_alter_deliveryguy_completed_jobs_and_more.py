# Generated by Django 4.1.4 on 2023-06-03 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_remove_deliveryguy_profile_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryguy',
            name='completed_jobs',
            field=models.CharField(default=0, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='deliveryguy',
            name='driven',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='deliveryguy',
            name='earnings',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
