# Generated by Django 5.1.2 on 2024-11-04 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_app', '0011_alter_users_id_alter_wallets_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]