from .base import *

# Disable debug mode
DEBUG = False

# Set your production domain(s) here
ALLOWED_HOSTS = ['your-domain.com']

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your-db-name',
        'USER': 'your-db-user',
        'PASSWORD': 'your-db-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static files configuration
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Media files configuration
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Security settings
SECRET_KEY = 'your-secret-key'

# Additional security settings (optional)
# ...

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-host'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'your-email@example.com'

# Logging configuration
# Configure logging handlers, loggers, and formatters here

# Other production-specific settings
# ...
