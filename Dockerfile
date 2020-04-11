FROM python:3.7-alpine as image_base

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apk add libffi-dev py-cffi \
  # Translations dependencies
  && apk add gettext \
  # https://docs.djangoproject.com/en/dev/ref/django-admin/#dbshell
  && apk add postgresql-client \
  && apk add linux-headers \
  && apk add libmemcached-dev \
  && apk add bash

COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/common.txt

COPY compose/post-build /post-build
RUN sed -i 's/\r//' /post-build
RUN chmod +x /post-build

EXPOSE 8000
WORKDIR /app

#
#  D E V E L O P M E N T
#
FROM image_base as development

RUN pip install -r /requirements/testing.txt
RUN pip install -r /requirements/develop.txt

COPY compose/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint


COPY compose/start-dev /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

# C E L E R Y

COPY compose/celery/dev/start-celeryworker /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY compose/celery/dev/start-celerybeat /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY compose/celery/dev/start-flower /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower


ENTRYPOINT ["/entrypoint"]

#
#  C I / C D
#
FROM development as ci_cd

RUN apk add make build-base
RUN pip install docker-compose awscli
