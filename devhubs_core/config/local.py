from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

MEDIA_URL = '/media/'


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  
]


CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://localhost:3000',
]