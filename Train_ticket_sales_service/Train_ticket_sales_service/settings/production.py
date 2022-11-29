from .base import *

DEBUG = False

STATIC_ROOT = 'static/'

ALLOWED_HOSTS = ['trains.fithanso.ru', 'www.trains.fithanso.ru']

INTERNAL_IPS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

PATH_TO_WKHTMLTOPDF_EXE = ''

PURCHASED_TICKETS_PDFS_PATH = os.path.join(MEDIA_ROOT, 'purchased_tickets', 'pdfs', '')

EMAIL_HOST = 'mail.hosting.reg.ru'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'customerservice@trains.fithanso.ru'
EMAIL_HOST_PASSWORD = 'scubastar123'
EMAIL_USE_TLS = True

PDF_GENERATION_MODE = 'realtime'
