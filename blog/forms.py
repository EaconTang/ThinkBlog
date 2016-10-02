import os

from django import forms
from django.conf import settings


class UploadFileForm(forms.Form):
    """
    form used to upload file
    """
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class UploadImageForm(forms.Form):
    """
    upload image to static_dir
    """
    static_image_path = os.path.join(getattr(settings, 'STATIC_ROOT'), 'image')
    image_dir = forms.FilePathField(path=static_image_path, recursive=True, allow_files=False, allow_folders=True,
                                     required=False)
    image_name = forms.CharField(max_length=32)
    image_file = forms.ImageField()
