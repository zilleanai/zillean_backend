#!/bin/sh

until flask db init
do
    echo "Waiting for postgres ready..."
    sleep 2
done

flask db migrate -m 'create initial tables'
flask db upgrade

flask run --host 0.0.0.0 --port 5000
