# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-29 19:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0012_logentry_request_counter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logentry',
            name='request_counter',
        ),
    ]
