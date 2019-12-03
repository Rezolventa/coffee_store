# Сoffee Store
A simple coffee store app with CRUD functionality as my first Django project.
# Getting started
Follow these simple instructions to get a copy of a project for personal use and testing.
## Prerequisites
To launch bot you have your MongoDB to be installed.
## Installing
Clone the repository, create a new virtual environment and install all dependencies from a requirements.txt file.
```
pip install -r requirements.txt
```
Link your database in coffee_store/coffee_store/settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER' : 'postgres',
        'PASSWORD' : '31337',
        'HOST' : '127.0.0.1',
        'PORT' : '5432',
    }
}
```
To start the server you want to run `manage.py` in `coffee_store` directory with `runserver` command:
```
cd coffee_store
python manage.py runserver
```
The default server port is 8000. The index page will be at `http://127.0.0.1:8000/`.
# Functionality
You can create, edit and delete coffee products, add them to a cart and confirm an order.
# Running the tests
To run automatic tests use `test` command. Specify the app name if tests do not start.
```
python manage.py test retail
```
