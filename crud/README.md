# Simple django crud #

The repository contains a simple crud with Django. It uses google auth to login and to manage bankusers and bankaccounts.

It uses:

- Django==2.0.4

- psycopg2==2.7.4

- python-social-auth==0.3.6

- social-auth-app-django==2.1.0

- django-bootstrap3==10.0.1

## Use with docker-compose
```
docker-compose up
```
> Note: 
>This project is prepared to run with docker-compose, so django default 
db settings are the credentials used with postgres in docker-compose.yml
 but django settings are prepared to get db data with environment variables
 
## Use with docker image
```
docker build -t django_crud .
```

settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('DB_HOST', "db"),
        'NAME': os.environ.get('DB_NAME', "users"),
        'USER': os.environ.get('DB_USER', "alexis"),
        'PASSWORD': os.environ.get('DB_PASS', "alexis"),
    }
}
```
```
 docker run -d -p 8000:8000 -e DB_HOST=myhost -e DB_NAME=mydb -e DB_USER=myuser -e DB_PASS=mypass -name django_crud django_crud
```


## Tests
To run the test execute
```
docker-compose run web python3 manage.py test core.tests
```

## Dependencies
    
[Django](https://www.djangoproject.com/)

[Docker](https://www.docker.com/)
