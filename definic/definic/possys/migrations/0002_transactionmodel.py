# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-27 07:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('possys', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tr_id', models.CharField(max_length=100)),
                ('Pos_num', models.CharField(max_length=100)),
                ('Item_id', models.CharField(max_length=100)),
                ('Tr_price', models.CharField(max_length=100)),
                ('Tr_quantity', models.CharField(max_length=100)),
                ('Tr_date', models.CharField(max_length=100)),
            ],
        ),
    ]