# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0012_siteinfo_site_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteinfo',
            name='site_about_me',
            field=models.TextField(verbose_name=b'About Me', blank=True),
        ),
    ]
