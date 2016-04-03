# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20160402_0329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mdfiletag',
            name='md_file',
        ),
        migrations.AddField(
            model_name='mdfiletag',
            name='md_file',
            field=models.ManyToManyField(related_name='md_tags_to_files', to='blog.MDFile'),
        ),
    ]
