release: python manage.py migrate
release: python manage.py collectstatic --noinput

web: gunicorn config.wsgi:application

worker: celery worker --app=config.celery_app --loglevel=info
beat: celery beat --app=config.celery_app --loglevel=info
