# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-19 20:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0032_sitevisit'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitevisit',
            name='day_visit',
            field=models.DateField(default=datetime.date(2017, 12, 19), verbose_name=b'Visit Date'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sitevisit',
            name='time_visit',
            field=models.DateTimeField(verbose_name=b'Visit Hour'),
        ),
    ]