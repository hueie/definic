# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-29 05:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('possys', '0005_delete_datawarehousemodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventorymodel',
            old_name='Date',
            new_name='Inv_date',
        ),
        migrations.RenameField(
            model_name='inventorymodel',
            old_name='Expense',
            new_name='Inv_expense',
        ),
        migrations.RenameField(
            model_name='inventorymodel',
            old_name='Item_id',
            new_name='Inv_item_id',
        ),
        migrations.RenameField(
            model_name='inventorymodel',
            old_name='Quantity',
            new_name='Inv_quantity',
        ),
    ]
