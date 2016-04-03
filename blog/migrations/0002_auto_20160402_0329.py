# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mdfile',
            name='md_category',
            field=models.ForeignKey(to='blog.MDFileCategory', null=True),
        ),
        migrations.AddField(
            model_name='mdfilecomment',
            name='md_file',
            field=models.ForeignKey(to='blog.MDFile', null=True),
        ),
        migrations.AddField(
            model_name='mdfiletag',
            name='md_file',
            field=models.ForeignKey(to='blog.MDFile', null=True),
        ),
        migrations.AlterField(
            model_name='mdfile',
            name='md_text',
            field=models.TextField(help_text=b'\n    Markdown\xe8\xaf\xad\xe6\xb3\x95\xe8\xaf\xb4\xe6\x98\x8e: http://www.jianshu.com/p/q81RER\n    ', blank=True),
        ),
    ]
