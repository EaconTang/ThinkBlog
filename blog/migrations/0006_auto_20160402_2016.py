# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20160402_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='mdfiletag',
            name='md_tag_urlname',
            field=models.CharField(default=b'untagged', unique=True, max_length=32, verbose_name=b'TagURLName'),
        ),
        migrations.AlterField(
            model_name='mdfiletag',
            name='md_tag_name',
            field=models.CharField(unique=True, max_length=32, verbose_name=b'TagName'),
        ),
        migrations.AlterField(
            model_name='siteinfo',
            name='site_version',
            field=models.CharField(default=b'0.0', max_length=32, verbose_name=b'Site Version'),
        ),
    ]
