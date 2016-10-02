# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0013_siteinfo_site_about_me'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteinfo',
            name='site_is_published',
            field=models.NullBooleanField(default=False, verbose_name=b'Published Version'),
        ),
    ]
