# Generated by Django 4.1.4 on 2023-06-11 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_remove_message_receiver_remove_message_sender_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='id',
        ),
        migrations.AlterField(
            model_name='message',
            name='message_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_type',
            field=models.CharField(default='feedback', max_length=20),
        ),
    ]
