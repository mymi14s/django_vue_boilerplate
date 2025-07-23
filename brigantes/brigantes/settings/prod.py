
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
# STATICFILES_DIRS = [STATIC_DIR,]s
MEDIA_ROOT = MEDIA_DIR
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Optional for WhiteNoise if you're not using it in prod
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
