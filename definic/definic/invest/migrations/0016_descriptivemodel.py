# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 04:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0015_auto_20170205_2229'),
    ]

    operations = [
        migrations.CreateModel(
            name='DescriptiveModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_code', models.CharField(max_length=100)),
                ('amean', models.FloatField()),
                ('hmean', models.FloatField()),
                ('gmean', models.FloatField()),
                ('median', models.FloatField()),
                ('mode', models.FloatField()),
                ('min', models.FloatField()),
                ('max', models.FloatField()),
                ('q1', models.FloatField()),
                ('q2', models.FloatField()),
                ('q3', models.FloatField()),
                ('var', models.FloatField()),
                ('std', models.FloatField()),
                ('cov', models.FloatField()),
                ('corr', models.FloatField()),
            ],
        ),
    ]