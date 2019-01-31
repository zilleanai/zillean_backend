FROM chriamue/flask-unchained
USER root
COPY ./mlplatform_backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./mlplatform_backend/requirements-dev.txt requirements-dev.txt
RUN pip install -r requirements-dev.txt

USER flask

RUN mkdir -p /flask/.cache /flask/.local/share

COPY ./docker/celery-beat-entrypoint.sh /
COPY ./docker/celery-worker-entrypoint.sh /
COPY ./docker/flask-entrypoint.sh /flask-entrypoint.sh