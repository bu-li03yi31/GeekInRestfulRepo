# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-18 00:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GeekInRest', '0002_auto_20170416_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertags',
            name='tid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GeekInRest.Tags'),
        ),
    ]
