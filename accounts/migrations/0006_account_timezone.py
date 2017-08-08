# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-10 18:23
from __future__ import unicode_literals

from django.db import migrations
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20170625_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(default='UTC', verbose_name='Time zone'),
        ),
    ]