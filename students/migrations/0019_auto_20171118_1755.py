# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-11-18 17:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0018_auto_20171115_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='students.Group', verbose_name='Group'),
        ),
    ]
