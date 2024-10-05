from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

MEDIA_URL = '/media/'

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    #'http://localhost:4321',
]