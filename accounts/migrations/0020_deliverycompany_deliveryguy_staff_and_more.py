# Generated by Django 4.1.6 on 2023-04-12 04:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_alter_account_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryCompany',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('username', models.CharField(max_length=100, null=True)),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('phone_number', models.IntegerField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('profile_image', models.ImageField(blank=True, default='profile/buyer/user-default.png', null=True, upload_to='profile/seller/')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryGuy',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('username', models.CharField(max_length=100, null=True)),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('phone_number', models.IntegerField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('profile_image', models.ImageField(blank=True, default='profile/buyer/user-default.png', null=True, upload_to='profile/seller/')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('username', models.CharField(max_length=100, null=True)),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('phone_number', models.IntegerField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('profile_image', models.ImageField(blank=True, default='profile/buyer/user-default.png', null=True, upload_to='profile/seller/')),
            ],
        ),
        migrations.RenameField(
            model_name='account',
            old_name='is_admin',
            new_name='is_delivery_company',
        ),
        migrations.AddField(
            model_name='account',
            name='is_delivery_guy',
            field=models.BooleanField(default=False),
        ),
    ]
