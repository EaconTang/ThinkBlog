# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0003_auto_20160402_0349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mdfiletag',
            name='md_file',
        ),
        migrations.AddField(
            model_name='mdfile',
            name='md_tag',
            field=models.ManyToManyField(related_name='md_files_to_tags', to='blog.MDFileTag'),
        ),
    ]
