# Simple django crud #

The repository contains simple crud with Django. It uses postgres as database and a google account to login.

It uses:

- Django==2.0.4

- psycopg2==2.7.4

- python-social-auth==0.3.6

- social-auth-app-django==2.1.0

- django-bootstrap3==10.0.1


## Use
```
docker build -t django_crud .
```
```
docker run -d -p 8000:8000 -name django_crud django_crud
```
> Note: 
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
>This project is prepared to run with docker-compose,  where you should run the postgres images with environament variables (see file docker-compose.yml)
>But you can execute the django image passing environment variables to use your own database
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
