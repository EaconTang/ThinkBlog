from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyBlog.settings")

# Celery Settings
CELERY_BROKER = 'redis://localhost:6379/0'
CELERY_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'Asia/Shanghai'

app = Celery('MyBlog',
             broker=CELERY_BROKER,
             backend=CELERY_BACKEND
             )
app.conf.update(
    task_serializer=CELERY_TASK_SERIALIZER,
    accept_content=CELERY_ACCEPT_CONTENT,  # Ignore other content
    timezone=CELERY_TIMEZONE,
)


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


