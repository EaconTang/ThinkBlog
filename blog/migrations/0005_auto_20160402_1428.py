# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0004_auto_20160402_0352'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site_version', models.CharField(default=b'1.0', max_length=32, verbose_name=b'Site Version')),
                ('site_visit', models.IntegerField(default=0, verbose_name=b'Site Visits')),
                ('site_copyright', models.TextField(null=True, verbose_name=b'Site copyright')),
            ],
        ),
        migrations.AlterField(
            model_name='mdfile',
            name='md_category',
            field=models.ForeignKey(verbose_name=b'Category', to='blog.MDFileCategory', null=True),
        ),
        migrations.AlterField(
            model_name='mdfile',
            name='md_filename',
            field=models.CharField(unique=True, max_length=128, verbose_name=b'Title'),
        ),
        migrations.AlterField(
            model_name='mdfile',
            name='md_mod_time',
            field=models.DateTimeField(null=True, verbose_name=b'Modify Time'),
        ),
        migrations.AlterField(
            model_name='mdfile',
            name='md_pub_time',
            field=models.DateTimeField(null=True, verbose_name=b'Publish Time'),
        ),
        migrations.AlterField(
            model_name='mdfile',
            name='md_tag',
            field=models.ManyToManyField(related_name='md_files_to_tags', verbose_name=b'Tags', to='blog.MDFileTag'),
        ),
        migrations.AlterField(
            model_name='mdfile',
            name='md_text',
            field=models.TextField(
                help_text=b'\n    Markdown\xe8\xaf\xad\xe6\xb3\x95\xe8\xaf\xb4\xe6\x98\x8e: http://www.jianshu.com/p/q81RER\n    ',
                verbose_name=b'Text', blank=True),
        ),
        migrations.AlterField(
            model_name='mdfile',
            name='md_url',
            field=models.CharField(unique=True, max_length=256, verbose_name=b'URL'),
        ),
        migrations.AlterField(
            model_name='mdfile',
            name='md_visit',
            field=models.IntegerField(null=True, verbose_name=b'Visits'),
        ),
        migrations.AlterField(
            model_name='mdfilecategory',
            name='md_category_name',
            field=models.CharField(unique=True, max_length=32, verbose_name=b'Category'),
        ),
        migrations.AlterField(
            model_name='mdfiletag',
            name='md_tag_name',
            field=models.CharField(unique=True, max_length=32, verbose_name=b'Tag'),
        ),
    ]
