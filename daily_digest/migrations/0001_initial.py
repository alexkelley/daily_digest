# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-23 02:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote_text', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('times_served', models.PositiveSmallIntegerField(default=0)),
                ('votes', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Quote_Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200)),
                ('biography_url', models.URLField()),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='daily_digest.Quote')),
            ],
        ),
    ]
