# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-05 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0014_auto_20170205_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preprocessormodel',
            name='split_ratio',
            field=models.FloatField(default=0.0, max_length=100),
        ),
    ]
