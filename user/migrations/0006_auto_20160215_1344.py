# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-15 13:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20160215_0840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='age',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='birthdate',
            field=models.DateField(blank=True, default=datetime.datetime(2016, 2, 15, 13, 44, 13, 464736, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
