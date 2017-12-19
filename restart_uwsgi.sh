#!/usr/bin/env bash
ps aux|grep uwsgi|grep -v grep|awk '{print $2}'|xargs kill -9
sleep 3
nohup uwsgi --ini uwsgi_blog.ini &
tail -f nohup.out