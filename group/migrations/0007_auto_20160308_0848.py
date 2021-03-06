# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-08 08:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0006_group_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='city',
            field=models.CharField(default='Lyon', max_length=60),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='groupstatus',
            name='status',
            field=models.CharField(choices=[('ADM', 'Admin'), ('MEM', 'Member'), ('PEN', 'Pending'), ('INV', 'Invited')], max_length=3),
        ),
    ]
