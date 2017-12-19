#!/usr/bin/env bash
python manage.py makemigrations
python manage.py migrate
sh restart_uwsgi.sh