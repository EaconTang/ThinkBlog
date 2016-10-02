# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0014_siteinfo_site_is_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteinfo',
            name='site_is_published',
            field=models.NullBooleanField(default=False, verbose_name=b'Published'),
        ),
    ]
