from .base import *

INSTALLED_APPS += ["debug_toolbar"]

DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = ['*']

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

# ==============================================================================
# MySQL Settings
# ==============================================================================
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'webiner',
#         'USER': 'root',
#         'PASSWORD': 'T3chlogicians.saadi12',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }


# ==============================================================================
# db.sqlite3 Settings
# ==============================================================================

EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = '0cc096e49cebc2'
EMAIL_HOST_PASSWORD = 'f1c98ba7bd13f5'
EMAIL_PORT = '2525'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
