# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-30 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0011_auto_20170530_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='pin_code',
            field=models.IntegerField(default=0, editable=False, max_length=10),
        ),
    ]