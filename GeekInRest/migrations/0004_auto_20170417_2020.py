# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-18 00:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GeekInRest', '0003_auto_20170417_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='email',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GeekInRest.Users'),
        ),
    ]