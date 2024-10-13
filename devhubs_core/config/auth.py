from datetime import timedelta
from decouple import config

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    #'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1  # Required for allauth

# JWT SimpleJWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'BLACKLIST_AFTER_ROTATION': True,
}

# Specify the user model for authentication
AUTH_USER_MODEL = 'users.User'

REST_USE_JWT = True

# AllAuth settings
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'  # Allow authentication using either username or email
ACCOUNT_EMAIL_REQUIRED = True  # Email is still required
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Optional email verification (or set to "mandatory")
ACCOUNT_USERNAME_REQUIRED = True  # Username is still required
ACCOUNT_UNIQUE_EMAIL = True  # Ensure that emails are unique
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True  # Log the user in after email confirmation
ACCOUNT_LOGOUT_ON_GET = True  # Allow immediate logout on GET request
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
#ACCOUNT_ADAPTER = 'authentication.adapters.CustomAccountAdapter' 

# Enable OAuth backends (Google & GitHub)
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID'),
            'secret': config('GOOGLE_CLIENT_SECRET'),
            'scope': ['profile', 'email'],
        }
    },
    'github': {
        'APP': {
            'client_id': config('GITHUB_CLIENT_ID'),
            'secret': config('GITHUB_CLIENT_SECRET'),
            'scope': ['user:email'],
        }
    },
}