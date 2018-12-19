FROM tensorflow/tensorflow:latest-py3

ENV PYTHONUNBUFFERED 1

RUN useradd --user-group --create-home --home-dir /flask --shell /bin/false flask

RUN apt-get update && apt-get install -y \
    build-essential libxml2-dev libxslt-dev libffi-dev postgresql postgresql-server-dev-all git gfortran libopenblas-dev libfreetype6-dev libpng-dev \
 && rm -rf /var/lib/apt/lists/*

RUN add-apt-repository -y ppa:jonathonf/python-3.6 \
 && apt-get update \
 && apt-get install -y python3.6 python3.6-dev python3-pip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && rm -f /usr/bin/python3 && ln -s /usr/bin/python3.6 /usr/bin/python3

RUN python -m pip install --no-cache-dir -U pip
RUN python -m pip install --no-cache-dir -U setuptools

WORKDIR /flask/src

COPY ./mlplatform_backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./mlplatform_backend/requirements-dev.txt requirements-dev.txt
RUN pip install --no-cache-dir -r requirements-dev.txt

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

USER flask

RUN mkdir -p /flask/.cache /flask/.local/share

COPY ./docker/celery-beat-entrypoint.sh /
COPY ./docker/celery-worker-entrypoint.sh /
COPY ./docker/flask-entrypoint.sh /flask-entrypoint.sh