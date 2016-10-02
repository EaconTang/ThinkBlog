# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-26 06:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0025_auto_20160723_2216'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(upload_to=b'', verbose_name=b'ImageFile')),
                ('image_name', models.CharField(max_length=32, verbose_name=b'ImageName')),
                ('image_path',
                 models.FilePathField(allow_folders=True, path=b'/Users/eacon/Study/_Python/MyBlog/static/image',
                                      recursive=True)),
                ('is_exported', models.BooleanField(default=False)),
            ],
        ),
    ]