# Generated by Django 4.1.4 on 2023-05-29 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_variation_variation_category'),
        ('orders', '0019_alter_orderedproduct_variations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderedproduct',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.variation'),
        ),
    ]
