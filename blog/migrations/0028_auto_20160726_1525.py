# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-26 07:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0027_auto_20160726_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagefile',
            name='image_file',
            field=models.ImageField(upload_to=b'', verbose_name=b'ImageFile'),
        ),
    ]
