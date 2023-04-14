#!/usr/bin/env bash

set -o errexit  # exit on error

pip install -r requirements.txt


python manage.py collectstatic --no-input
python manage.py migrate

#python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('YOUR_USERNAME', 'YOUR_EMAIL', 'YOUR_PASSWORD') if not User.objects.filter(username='YOUR_USERNAME').exists() else None"


#python3 manage.py test catalog.tests --verbosity 2      


#sudo -u postgres createuser -s alumnodb
#sudo -u postgres psql -c "ALTER USER alumnodb WITH PASSWORD 'alumnodb';"

#python manage.py collectstatic



