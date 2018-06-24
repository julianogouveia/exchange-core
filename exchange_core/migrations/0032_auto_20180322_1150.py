# Generated by Django 2.0.2 on 2018-03-22 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_core', '0031_auto_20180320_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='mobile_phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='bankaccounts',
            name='account_number_digit',
            field=models.CharField(
                max_length=5, null=True, verbose_name='Digit'),
        ),
        migrations.AlterField(
            model_name='bankaccounts',
            name='agency_digit',
            field=models.CharField(
                max_length=5, null=True, verbose_name='Digit'),
        ),
    ]
