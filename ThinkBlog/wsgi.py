"""
WSGI config for ThinkBlog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ThinkBlog.settings")

application = get_wsgi_application()
