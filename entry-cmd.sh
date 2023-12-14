#!/bin/bash

su -c "icecast -c /code/icecast.xml" icecast &
python3 manage.py runserver 0.0.0.0:8100 &

wait -n
exit $?