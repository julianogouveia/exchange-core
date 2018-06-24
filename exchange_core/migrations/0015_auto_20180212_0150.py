# Generated by Django 2.0.2 on 2018-02-12 01:50

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_core', '0014_auto_20180212_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencies',
            name='withdraw_fee',
            field=models.DecimalField(decimal_places=8, default=Decimal(
                '0.005'), max_digits=20, verbose_name='Withdraw Fee'),
        ),
        migrations.AlterField(
            model_name='currencies',
            name='withdraw_max',
            field=models.DecimalField(decimal_places=8, default=Decimal(
                '1000000.00'), max_digits=20, verbose_name='Withdraw Max'),
        ),
        migrations.AlterField(
            model_name='currencies',
            name='withdraw_min',
            field=models.DecimalField(decimal_places=8, default=Decimal(
                '0.001'), max_digits=20, verbose_name='Withdraw Min'),
        ),
    ]
