# Generated by Django 2.0.1 on 2018-03-20 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_core', '0030_auto_20180320_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankwithdraw',
            name='account_number_digit',
            field=models.CharField(
                max_length=5, null=True, verbose_name='Account number digit'),
        ),
        migrations.AddField(
            model_name='bankwithdraw',
            name='agency_digit',
            field=models.CharField(
                max_length=5, null=True, verbose_name='Agency Digit'),
        ),
        migrations.AlterField(
            model_name='addresses',
            name='address',
            field=models.CharField(max_length=100, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='addresses',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='addresses', to=settings.CITIES_CITY_MODEL, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='addresses',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='addresses', to=settings.CITIES_COUNTRY_MODEL, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='addresses',
            name='neighborhood',
            field=models.CharField(max_length=50, verbose_name='neighborhood'),
        ),
        migrations.AlterField(
            model_name='addresses',
            name='number',
            field=models.CharField(max_length=20, verbose_name='Number'),
        ),
        migrations.AlterField(
            model_name='addresses',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='addresses', to='cities.Region', verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='addresses',
            name='type',
            field=models.CharField(choices=[(
                'account', 'account')], default='account', max_length=20, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='addresses',
            name='zipcode',
            field=models.CharField(max_length=10, verbose_name='Zipcode'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='type',
            field=models.CharField(choices=[('deposit', 'deposit'), ('reverse', 'reverse'), ('withdraw', 'withdraw'), (
                'income', 'income'), ('investment', 'investment')], max_length=30, verbose_name='Type'),
        ),
    ]
