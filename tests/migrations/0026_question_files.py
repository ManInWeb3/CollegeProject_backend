# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-07 16:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0025_auto_20170806_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='files',
            field=models.FileField(blank=True, null=True, upload_to='attachments'),
        ),
    ]