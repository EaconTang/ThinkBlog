# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0009_auto_20160402_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='mdfile',
            name='md_summary',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mdfile',
            name='md_tag',
            field=models.ManyToManyField(default=b'untagged', to='blog.MDFileTag', null=True, verbose_name=b'Tag'),
        ),
    ]
