# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0006_auto_20160402_2016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mdfiletag',
            name='md_tag_urlname',
        ),
        migrations.AddField(
            model_name='mdfilecategory',
            name='md_category_url',
            field=models.CharField(default=b'uncategorized', unique=True, max_length=32, verbose_name=b'CategoryURL'),
        ),
        migrations.AddField(
            model_name='mdfiletag',
            name='md_tag_url',
            field=models.CharField(default=b'untagged', unique=True, max_length=32, verbose_name=b'TagURL'),
        ),
        migrations.AlterField(
            model_name='mdfilecategory',
            name='md_category_name',
            field=models.CharField(unique=True, max_length=32, verbose_name=b'CategoryName'),
        ),
    ]
