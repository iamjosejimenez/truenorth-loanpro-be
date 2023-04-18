README

export DJANGO_READ_DOT_ENV_FILE=False

export DJANGO_SETTINGS_MODULE=loanpro_be.local

poetry run python manage.py load_default_data

# Introduction

Django based backend solution to **truenorth loanpro challenge**, made by José Luis Jiménez. Live version can be found [here](https://rr4llqyhrl.execute-api.us-east-2.amazonaws.com/production/api/docs/). Deployed serverless using AWS lambdas.

Written in django 4.2 and python 3.9. Sqlite was used for local development, and postgresql in production.

### Main features

- Static files are served using S3.

- Env files are used for production configuration.

- Endpoint configuration was done with Django Rest Framework, including authentication, pagination, sorting and searching.

- Poetry used for project's dependencies.
  

# Usage

### Prerequisites

Install Python 3.9:

    $ https://www.python.org/downloads/release/python-3916/

Install Poetry.

    $ pip install poetry

# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone git@github.com:iamjosejimenez/truenorth-loanpro-be.git
    $ cd truenorth-loanpro-be

Install project dependencies:

    $ poetry install

Activate virtualenv:

    $ source $(poetry env info --path)/bin/activate

Create environment variables:

    $ export DJANGO_SETTINGS_MODULE=loanpro_be.local
    $ export DJANGO_READ_DOT_ENV_FILE=False

Apply migrations:

    $ python manage.py migrate

Create superuser for authenticated endpoints and frontend access, use any email and password:

    $ python manage.py createsuperuser

Load initial data:
    
    $ python manage.py load_default_data

You can now run the development server:

    $ python manage.py runserver
