#!/bin/bash

if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for mysql..."
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done
    echo "MySQL started"
fi








echo "Appling database migrations..."
python manage.py makemigrations 
python manage.py migrate

echo $ADMIN_NAME


echo "from django.contrib.auth.models import User; User.objects.create_superuser('${ADMIN_NAME}', \
'admin@example.com', '${ADMIN_PASSWORD}') if len(User.objects.filter(username='${ADMIN_NAME}'))==0 \
else print('user exist')" | python manage.py shell


exec "$@"
