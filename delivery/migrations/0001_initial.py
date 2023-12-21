# Generated by Django 4.1.4 on 2023-04-26 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0021_remove_deliverycompany_location_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('InProgress', 'InProgress'), ('Completed', 'Completed')], default='InProgress', max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date_added', models.DateField(auto_now_add=True, null=True)),
                ('delivery_person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.deliveryguy')),
                ('reciver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.buyer')),
            ],
        ),
    ]
