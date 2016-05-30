import os

from .settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'oneliner',
        'USER': 'oneliner',
        'PASSWORD': os.environ['ONELINER_PROD_DB_PASSWORD'],
        'HOST': 'localhost',
        'PORT': '3306',
    },
}
