#!/bin/bash

PROJECT=oneliner
USE_ACCOUNT=www-data

GUNICORN=/home/newsapps/.virtualenvs/$PROJECT/bin/gunicorn
ROOT=/home/newsapps/sites/$PROJECT
PID=/var/run/${PROJECT}.pid
ADDRESS=127.0.0.1:8080
ERROR_LOG=/home/newsapps/logs/${PROJECT}.error.log
WSGI_MODULE="${PROJECT}.wsgi"

. /home/newsapps/secrets/all_secrets.sh

if [ -f $PID ]
then
    rm $PID
fi

cd $ROOT
exec $GUNICORN --bind=$ADDRESS --workers=1 \
    --keep-alive=0 --max-requests=1000 --user=www-data \
    --group=$USE_ACCOUNT --name=$PROJECT \
    --worker-class=gevent --error-logfile=$ERROR_LOG \
    $WSGI_MODULE
