web: gunicorn --bind=0.0.0.0 --log-file - td.wsgi
worker: celery worker --app=td --concurrency=4 --pool=prefork --no-color