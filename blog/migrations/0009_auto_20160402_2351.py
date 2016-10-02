# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0008_auto_20160402_2334'),
    ]

    operations = [
        migrations.CreateModel(
            name='MDFileCategoryURL',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('md_category_url', models.CharField(max_length=64)),
                ('md_category_name', models.OneToOneField(to='blog.MDFileCategory')),
            ],
            options={
                'verbose_name': '\u5206\u7c7b-\u7f51\u5740',
                'verbose_name_plural': '\u5206\u7c7b-\u7f51\u5740',
            },
        ),
        migrations.AlterModelOptions(
            name='mdfiletagurl',
            options={'verbose_name': '\u6807\u7b7e-\u7f51\u5740', 'verbose_name_plural': '\u6807\u7b7e-\u7f51\u5740'},
        ),
        migrations.RemoveField(
            model_name='mdfile',
            name='md_category',
        ),
        migrations.AddField(
            model_name='mdfile',
            name='md_category',
            field=models.ManyToManyField(default=b'uncategorized', to='blog.MDFileCategory', null=True,
                                         verbose_name=b'Category'),
        ),
    ]
