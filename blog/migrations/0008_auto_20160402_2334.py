# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0007_auto_20160402_2212'),
    ]

    operations = [
        migrations.CreateModel(
            name='MDFileTagURL',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('md_tag_url', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': '\u6807\u7b7e\u7f51\u5740',
                'verbose_name_plural': '\u6807\u7b7e\u7f51\u5740',
            },
        ),
        migrations.AlterModelOptions(
            name='mdfile',
            options={'verbose_name': '\u535a\u5ba2', 'verbose_name_plural': '\u535a\u5ba2'},
        ),
        migrations.AlterModelOptions(
            name='mdfilecategory',
            options={'verbose_name': '\u5206\u7c7b', 'verbose_name_plural': '\u5206\u7c7b'},
        ),
        migrations.AlterModelOptions(
            name='mdfilecomment',
            options={'verbose_name': '\u8bc4\u8bba', 'verbose_name_plural': '\u8bc4\u8bba'},
        ),
        migrations.AlterModelOptions(
            name='mdfiletag',
            options={'verbose_name': '\u6807\u7b7e', 'verbose_name_plural': '\u6807\u7b7e'},
        ),
        migrations.AlterModelOptions(
            name='siteinfo',
            options={'verbose_name': '\u7f51\u7ad9\u4fe1\u606f', 'verbose_name_plural': '\u7f51\u7ad9\u4fe1\u606f'},
        ),
        migrations.RemoveField(
            model_name='mdfilecategory',
            name='md_category_url',
        ),
        migrations.RemoveField(
            model_name='mdfiletag',
            name='md_tag_url',
        ),
        migrations.AlterField(
            model_name='mdfile',
            name='md_category',
            field=models.ForeignKey(default=b'uncategorized', verbose_name=b'Category', to='blog.MDFileCategory',
                                    null=True),
        ),
        migrations.AlterField(
            model_name='mdfile',
            name='md_mod_time',
            field=models.DateTimeField(auto_now=True, verbose_name=b'Modify Time', null=True),
        ),
        migrations.AlterField(
            model_name='mdfile',
            name='md_tag',
            field=models.ManyToManyField(default=b'untagged', related_name='md_files_to_tags', verbose_name=b'Tags',
                                         to='blog.MDFileTag'),
        ),
        migrations.AddField(
            model_name='mdfiletagurl',
            name='md_tag_name',
            field=models.OneToOneField(to='blog.MDFileTag'),
        ),
    ]
