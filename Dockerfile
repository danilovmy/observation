FROM python:latest

## Create a group and user

WORKDIR /observations
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

## Install and test.
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py loaddata observations monitoreds

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
