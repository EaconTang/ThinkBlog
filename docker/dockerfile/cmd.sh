#!/usr/bin/env bash
/etc/init.d/redis-server start

sleep 2

cd /opt/ThinkBlog
celery worker -A ThinkBlog --loglevel info --logfile /opt/ThinkBlog/logs/celery_worker.log &
python manage.py runserver 0.0.0.0:8000