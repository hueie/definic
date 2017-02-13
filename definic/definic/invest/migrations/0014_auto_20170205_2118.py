# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-05 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0013_preprocessormodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='preprocessormodel',
            name='stock_code',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='preprocessormodel',
            name='split_ratio',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='preprocessormodel',
            name='test',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='preprocessormodel',
            name='train',
            field=models.CharField(default='', max_length=100),
        ),
    ]