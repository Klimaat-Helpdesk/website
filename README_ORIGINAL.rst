Helpdesk Climate
================

This repository holds the code for https://helpdesk-climate.org, a website aimed at answering questions regarding climate
change, global warming, and related. This project was built using Django & Wagtail.

:License: MIT

Getting Started
---------------
Spin up docker containers with all the necessary dependencies. You will need docker-compose installed on your system::

    $ docker-compose -f local.yml build
    $ docker-compose -f local.yml up -d

The last command will spin up the containers and the website will be accessible through http://localhost:8000. If you remove the ``-d``, you will see the logs on screen, but the website will run only while your terminal is open.

Setting Up A Super User
^^^^^^^^^^^^^^^^^^^^^^^
Since we are using Wagtail as a CMS, we need to start by creating a super user::

    $ docker-compose -f local.yml run --rm django python manage.py createsuperuser

Follow the steps on screen, and then head to http://localshot:8000/cms to log in.

Deployment
----------
This website can be deployed using Docker. It will set up Django behind a Gunicorn worker, Traefik as a reverse proxy, Celery and Redis which are currently not in used in this project, but available in case they are needed.

Create a folder called ``.production`` in ``.envs``, add two files: **.django** and **.postgres**. The Django config file should hold the settings for the website::

    DJANGO_READ_DOT_ENV_FILE=True
    DJANGO_SETTINGS_MODULE=config.settings.production
    DJANGO_SECRET_KEY=
    DJANGO_ADMIN_URL=
    DJANGO_ALLOWED_HOSTS=

    DJANGO_SECURE_SSL_REDIRECT=False

    MAILGUN_API_KEY=
    DJANGO_SERVER_EMAIL=
    MAILGUN_DOMAIN=
    MAILGUN_API_URL=

    DJANGO_AWS_ACCESS_KEY_ID=
    DJANGO_AWS_SECRET_ACCESS_KEY=
    DJANGO_AWS_STORAGE_BUCKET_NAME=

    DJANGO_ACCOUNT_ALLOW_REGISTRATION=True

    WEB_CONCURRENCY=

    REDIS_URL=

    CELERY_FLOWER_USER=
    CELERY_FLOWER_PASSWORD=

And the postgres::

    POSTGRES_HOST=
    POSTGRES_PORT=
    POSTGRES_DB=
    POSTGRES_USER=
    POSTGRES_PASSWORD=


Docker
^^^^^^

    $ docker-compose -f production.yml build
    $ docker-compose -f production.yml up -d

