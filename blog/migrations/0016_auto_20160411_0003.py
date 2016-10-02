# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0015_auto_20160406_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisqusComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('md_comment_author', models.CharField(default=b'Anonymous', max_length=32, blank=True)),
                ('md_comment_mail', models.EmailField(max_length=254, blank=True)),
                ('md_comment_time', models.DateTimeField(null=True, verbose_name=b'comment time')),
                ('md_comment', models.TextField()),
            ],
            options={
                'abstract': False,
                'verbose_name': '\u8bc4\u8bba',
                'verbose_name_plural': '\u8bc4\u8bba',
            },
        ),
        migrations.CreateModel(
            name='DuoshuoComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('md_comment_author', models.CharField(default=b'Anonymous', max_length=32, blank=True)),
                ('md_comment_mail', models.EmailField(max_length=254, blank=True)),
                ('md_comment_time', models.DateTimeField(null=True, verbose_name=b'comment time')),
                ('md_comment', models.TextField()),
            ],
            options={
                'abstract': False,
                'verbose_name': '\u8bc4\u8bba',
                'verbose_name_plural': '\u8bc4\u8bba',
            },
        ),
        migrations.RemoveField(
            model_name='mdfilecomment',
            name='md_file',
        ),
        migrations.AlterModelOptions(
            name='mdfile',
            options={'ordering': ['-md_pub_time'], 'get_latest_by': '-md_pub_time', 'verbose_name': '\u535a\u5ba2',
                     'verbose_name_plural': '\u535a\u5ba2'},
        ),
        migrations.DeleteModel(
            name='MDFileComment',
        ),
        migrations.AddField(
            model_name='duoshuocomment',
            name='md_file',
            field=models.ForeignKey(to='blog.MDFile', null=True),
        ),
        migrations.AddField(
            model_name='disquscomment',
            name='md_file',
            field=models.ForeignKey(to='blog.MDFile', null=True),
        ),
    ]
