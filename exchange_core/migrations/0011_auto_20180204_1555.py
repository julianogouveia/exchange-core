# Generated by Django 2.0.1 on 2018-02-04 15:55

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_core', '0010_users_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='profile',
            field=django.contrib.postgres.fields.jsonb.JSONField(
                blank=True, default={}, null=True),
        ),
    ]
