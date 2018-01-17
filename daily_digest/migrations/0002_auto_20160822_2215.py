# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-23 03:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('daily_digest', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote_author',
            name='quote',
        ),
        migrations.AddField(
            model_name='quote',
            name='quote_author_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='daily_digest.Quote_Author'),
        ),
    ]