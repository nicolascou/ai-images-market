# Generated by Django 4.1.3 on 2023-02-02 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_customer_inventory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='item',
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(to='store.product'),
        ),
    ]
