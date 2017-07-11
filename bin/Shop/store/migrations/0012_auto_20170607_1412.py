# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-07 14:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20170607_1331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='gds',
        ),
        migrations.AddField(
            model_name='gds',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Order'),
        ),
    ]
