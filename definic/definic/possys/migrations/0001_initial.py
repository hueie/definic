# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-27 03:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataWareHouseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('In_out', models.CharField(max_length=100)),
                ('From_to', models.CharField(max_length=100)),
                ('Item_id', models.CharField(max_length=100)),
                ('Expense', models.CharField(max_length=100)),
                ('Quantity', models.CharField(max_length=100)),
                ('Date', models.CharField(max_length=100)),
            ],
        ),
    ]
