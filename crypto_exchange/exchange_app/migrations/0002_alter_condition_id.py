# Generated by Django 5.1.2 on 2024-11-02 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condition',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]