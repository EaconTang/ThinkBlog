# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MDFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('md_url', models.CharField(unique=True, max_length=256)),
                ('md_filename', models.CharField(unique=True, max_length=128)),
                ('md_text', models.TextField(blank=True)),
                ('md_pub_time', models.DateTimeField(null=True, verbose_name=b'publish date')),
                ('md_mod_time', models.DateTimeField(null=True, verbose_name=b'modify date')),
                ('md_modified', models.NullBooleanField()),
                ('md_visit', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MDFileCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('md_category_name', models.CharField(unique=True, max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='MDFileComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('md_comment_author', models.CharField(default=b'Anonymous', max_length=32, blank=True)),
                ('md_comment_mail', models.EmailField(max_length=254, blank=True)),
                ('md_comment_time', models.DateTimeField(null=True, verbose_name=b'comment time')),
                ('md_comment', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MDFileTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('md_tag_name', models.CharField(unique=True, max_length=32)),
            ],
        ),
    ]
