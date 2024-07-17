from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'MovieSite222',
        'USER': 'ernazar',
        'PASSWORD': '200100',
        'HOST': 'localhost',  # Replace with your PostgreSQL server's address if necessary
        'PORT': '5432',          # Leave empty to use the default PostgreSQL port (usually 5432)
    }
}
