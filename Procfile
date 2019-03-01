web: gunicorn --log-file - td.wsgi
worker: celery worker --app=td --concurrency=${CELERY_WORKER_COUNT:-2} --pool=prefork --no-color --loglevel=info --beat
