#!/bin/bash

set -eux

PATH=$PATH:/home/app/.local/bin

if [[ $DYNO == "web"* ]]; then
  gunicorn --log-file - td.wsgi
elif  [[ $DYNO == "worker"* ]]; then
  celery worker --app=td --autoscale=1,${CELERY_WORKER_COUNT:-2} --pool=prefork --no-color --loglevel=info --beat --maxtasksperchild=10
fi
