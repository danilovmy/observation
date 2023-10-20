FROM alpine:3, 3.18, 3.18.0, latest

## Create a group and user

WORKDIR ..

## Install and test.
RUN pip install -f requirements.txt
cd app
RUN python manage.py shemamigrations
RUN python manage.py migrate
RUN python manage.py loadfixtures

CMD ['python', 'manage.py', 'runserver', '0.0.0.0:8000']
