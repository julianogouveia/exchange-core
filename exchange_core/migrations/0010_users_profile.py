# Generated by Django 2.0.1 on 2018-02-03 17:55

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_core', '0009_auto_20180130_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='profile',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]