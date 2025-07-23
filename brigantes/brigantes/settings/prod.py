
from .base import *

DEBUG = False

ALLOWED_HOSTS = ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1']



# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv("DJANGO_DATABASE_URL")
    )
}