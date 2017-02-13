# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-05 10:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0011_alphamodelmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortfolioBuilderModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('df_stationarity', models.CharField(max_length=100)),
                ('df_rank', models.CharField(max_length=100)),
                ('stationarity_codes', models.CharField(max_length=100)),
                ('df_machine_result', models.CharField(max_length=100)),
                ('df_machine_rank', models.CharField(max_length=100)),
                ('machine_codes', models.CharField(max_length=100)),
            ],
        ),
    ]