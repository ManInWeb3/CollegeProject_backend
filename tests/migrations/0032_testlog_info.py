# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-15 13:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0031_auto_20170813_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='testlog',
            name='info',
            field=models.CharField(blank=True, default='', editable=False, max_length=50),
        ),
    ]
