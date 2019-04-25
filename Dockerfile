FROM zilleanai/flask-unchained:buster
USER root
RUN apt install -y python3-opencv
RUN pip install numpy Cython
RUN pip install git+https://github.com/zilleanai/zillean_cli
COPY ./zillean_backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./zillean_backend/requirements-dev.txt requirements-dev.txt
RUN pip install -r requirements-dev.txt

USER flask

RUN mkdir -p /flask/.cache /flask/.local/share

COPY  --chown=flask ./zillean_backend/ /flask/src/
COPY ./docker/celery-beat-entrypoint.sh /
COPY ./docker/celery-worker-entrypoint.sh /
COPY ./docker/flask-entrypoint.sh /flask-entrypoint.sh
ENTRYPOINT ["/flask-entrypoint.sh"]

