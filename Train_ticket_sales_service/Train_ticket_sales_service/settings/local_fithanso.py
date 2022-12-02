from .base import *
from decouple import config

DEBUG = True
INSTALLED_APPS += ['debug_toolbar']

ALLOWED_HOSTS = ['127.0.0.1']

INTERNAL_IPS = ['127.0.0.1']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

PATH_TO_WKHTMLTOPDF_EXE = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'

PURCHASED_TICKETS_PDFS_PATH = os.path.join(MEDIA_ROOT, 'purchased_tickets', 'pdfs', '')

EMAIL_HOST = 'localhost'
EMAIL_PORT = '1025'
EMAIL_USE_TLS = False

PDF_GENERATION_MODE = 'async'

CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"


EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

MEDIA_URL = 'https://storage.yandexcloud.net/trains-media-bucket/'
