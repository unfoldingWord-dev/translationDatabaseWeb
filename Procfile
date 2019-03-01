web: gunicorn --log-file - td.wsgi
worker: celery worker --app=td --autoscale=1,${CELERY_WORKER_COUNT:-2} --pool=prefork --no-color --loglevel=info --beat --maxtasksperchild=10
