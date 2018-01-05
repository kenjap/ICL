# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-02 20:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_article_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='publish',
            field=models.DateField(default=datetime.datetime(2018, 1, 2, 20, 1, 21, 997093, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
