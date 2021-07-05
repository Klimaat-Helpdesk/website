#FROM ubuntu:18.04
FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1

ENV TZ=Europe/Amsterdam
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update \
    && apt-get -y install wget gnupg python3 python3-pip python3-dev

RUN python3 -m pip install --upgrade pip

RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt bionic-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -


RUN apt-get update \
  && apt-get install -y gcc libpq-dev  \
  # Pillow dependencies
  libjpeg-dev zlib1g \
  # Translations dependencies
  gettext \
  # Postgres
#  libicu60 postgresql-12 postgresql-client-12 \
  # Git for cloning dependencies
  git curl


#RUN curl -sL https://deb.nodesource.com/setup_current.x | bash -
#RUN apt-get install -y nodejs
#
#RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
#
#RUN sh -c 'echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list'
#
#RUN apt-get update && \
#    apt-get -y install yarn
#
# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

#COPY ./yarn.lock /yarn.lock
#COPY ./package.json /package.json
#RUN yarn install

WORKDIR /app


ENTRYPOINT ["/entrypoint"]

