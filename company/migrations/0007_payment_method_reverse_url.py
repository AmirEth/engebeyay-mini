# Generated by Django 5.0 on 2023-12-25 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_remove_message_id_alter_message_message_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment_method',
            name='reverse_url',
            field=models.TextField(null=True),
        ),
    ]
