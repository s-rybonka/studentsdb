# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-29 18:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0011_auto_20170329_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='request_counter',
            field=models.IntegerField(default=0),
        ),
    ]
