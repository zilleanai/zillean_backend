#!/bin/sh

test -e app/config.py || (
   echo "WARNING: config.py not found, using default" &&\
   cp app/config.example.py app/config.py
)

until flask db upgrade
do
    echo "Waiting for postgres ready..."
    sleep 2
    flask db init
    flask db migrate -m 'create initial tables'
done

API_HOST="backend" flask run --host 0.0.0.0 --port 5000
