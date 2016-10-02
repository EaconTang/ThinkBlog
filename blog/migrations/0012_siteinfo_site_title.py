# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0011_mdfile_md_draft'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteinfo',
            name='site_title',
            field=models.CharField(max_length=32, verbose_name=b'Site Title', blank=True),
        ),
    ]
