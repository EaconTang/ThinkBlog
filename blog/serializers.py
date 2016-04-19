# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import MDFile

class MDFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MDFile
        fields = ('md_url', 'md_filename', 'md_pub_time', 'md_visit', 'tags', 'md_text', 'md_draft')
