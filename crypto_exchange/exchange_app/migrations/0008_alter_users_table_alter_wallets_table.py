# Generated by Django 5.1.2 on 2024-11-04 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_app', '0007_wallets_alter_users_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='users',
            table='users',
        ),
        migrations.AlterModelTable(
            name='wallets',
            table='wallets',
        ),
    ]
