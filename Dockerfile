FROM node:18-buster-slim as frontend
WORKDIR /home/userapp/src

RUN chown -R node:node /home/userapp
USER node

COPY --chown=node:node . /home/userapp/src

RUN yarn install && \
    yarn build

FROM docker-registry.fourdigits.nl/fourdigits-public/django-base-image:310 as production
ARG RELEASE_VERSION
ENV RELEASE_VERSION=$RELEASE_VERSION
ENV DJANGO_SETTINGS_MODULE=settings.production
WORKDIR /home/userapp/src

COPY --chown=userapp requirements /home/userapp/requirements
RUN pip install --upgrade pip gunicorn && pip install -r /home/userapp/requirements/production.txt

COPY --chown=userapp . /home/userapp/src
COPY --chown=userapp --from=frontend /home/userapp/src/apps/frontend/static /home/userapp/src/apps/frontend/static

CMD ["gunicorn", "settings.wsgi:application"]
