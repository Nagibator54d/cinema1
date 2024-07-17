from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Movavi',
        'USER': 'erkosh',
        'PASSWORD': '15072024',
        'HOST': 'localhost',  # Replace with your PostgreSQL server's address if necessary
        'PORT': '5432',          # Leave empty to use the default PostgreSQL port (usually 5432)
    }
}
