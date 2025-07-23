import os
from pathlib import Path
import dj_database_url
from datetime import timedelta


from dotenv import load_dotenv
from dotenv import dotenv_values

load_dotenv()

config = dotenv_values(".env")


ACCOUNT_SIGNUP_FIELDS = ['email', 'password1*', 'password2*']
ACCOUNT_LOGIN_METHODS = ["email"]
ACCOUNT_USER_MODEL_USERNAME_FIELD = None 

ACCOUNT_ADAPTER = 'user_management.adapters.NoSignupAccountAdapter'

ACCOUNT_FORMS = {
    'signup': 'user_management.forms.MyCustomSignupForm',
}






REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication', # Recommended for modern APIs
        'rest_framework.authentication.SessionAuthentication', # For browsable API and traditional web views
        'rest_framework.authentication.TokenAuthentication', # If you prefer simple token auth
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        
        'rest_framework.authentication.SessionAuthentication',
    ]
}

SITE_ID = 1

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'my-app-auth', # Name of the cookie for JWT
    'JWT_AUTH_REFRESH_COOKIE': 'my-refresh-token', # Name of the cookie for refresh token
}

# For djangorestframework-simplejwt (if USE_JWT is True in REST_AUTH)

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': config.get("DJANGO_SECRET_KEY") or os.environ.get('DJANGO_SECRET_KEY') or os.getenv("DJANGO_SECRET_KEY"), # Use your Django project's SECRET_KEY
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


