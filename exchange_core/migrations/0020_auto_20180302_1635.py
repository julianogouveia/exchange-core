# Generated by Django 2.0.2 on 2018-03-02 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_core', '0019_auto_20180302_1207'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bankwithdraw',
            old_name='profit',
            new_name='fee',
        ),
        migrations.RenameField(
            model_name='cryptowithdraw',
            old_name='profit',
            new_name='fee',
        ),
    ]