# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-05 23:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0004_auto_20170506_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='pass_date',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='date passed'),
        ),
        migrations.AlterField(
            model_name='test',
            name='pub_date',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='date created'),
        ),
    ]