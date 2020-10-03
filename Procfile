release: yarn webpack
release: python manage.py migrate
release: python manage.py collectstatic

web: gunicorn klimaat_helpdesk.wsgi
