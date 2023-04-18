README

export DJANGO_READ_DOT_ENV_FILE=False

export DJANGO_SETTINGS_MODULE=loanpro_be.local

poetry run python manage.py load_default_data
