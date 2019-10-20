School Students Management
====================

## Author

__Ahsanuzzaman Khan__

## Overview:
According to the usecase, I didn't bother with fancy UI as well as ajax call. It can be improved by implementing lot 
of things. I was just concentrating the basic workflow (CRUD functionality). Thus I use Django framework and PostgreSQL.


## Requirements
- Python 3.7
- PostgreSQL
- Django
- Django REST Framework
- Faker
- DRF Nested Routers

## Developer requirements
- Factory Boy
- Pytest Django

## Installation
- Install `pipenv`
- Download this git repo
- Then go to project directory
- And run `pipenv install`

## To Run project
Go to project folder and run 
- `pipenv shell`
- `python manage.py migrate`
- `python manage.py runserver`

## Test project
Go to project folder and run `pytest`

## Populate data with faker library
Go to project folder and run
- `pipenv shell`
- `python populate_data.py`
