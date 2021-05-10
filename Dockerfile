FROM python:3.8-slim-buster as image_base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONDEBUG 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext bash \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip

COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/common.txt

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

ENTRYPOINT ["/entrypoint"]

#
#  C I / C D
#
FROM development as ci_cd

RUN apk add make build-base
RUN pip install docker-compose awscli
