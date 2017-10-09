#!/bin/sh
set -e

export PGPASSWORD=$RDS_PASSWORD

while ! psql -h $RDS_HOSTNAME -d $RDS_DB_NAME -p $RDS_PORT -U $RDS_USERNAME -c "SELECT version();" > /dev/null 2>&1; do
    echo 'Waiting for connection with db...'
    sleep 1;
done;
echo 'Connected to db...';

if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
    python manage.py migrate --noinput
fi

if [ "x$DJANGO_MANAGEPY_COLLECTSTATIC" = 'xon' ]; then
    python manage.py collectstatic --noinput
fi

if [ "x$DJANGO_MANAGEPY_UPDATEINDEX" = 'xon' ]; then
    python manage.py update_index
fi

exec "$@"