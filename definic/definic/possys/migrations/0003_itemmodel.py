# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-27 08:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('possys', '0002_transactionmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Item_id', models.CharField(max_length=100)),
                ('Item_name', models.CharField(max_length=100)),
                ('Barcode', models.CharField(max_length=100)),
                ('Cur_price', models.CharField(max_length=100)),
                ('Cur_quantity', models.CharField(max_length=100)),
                ('Cur_place', models.CharField(max_length=100)),
                ('Item_date', models.CharField(max_length=100)),
            ],
        ),
    ]
