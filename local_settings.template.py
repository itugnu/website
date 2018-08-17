from itugnu.base import INSTALLED_APPS, MIDDLEWARE  # NOQA
import os
import raven

DEBUG = False
DEBUG_TOOLBAR = False

# Email Settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = ""
EMAIL_PORT = 465
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_SSL = True
# EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = ""
DEFAULT_CONTACT_EMAIL = DEFAULT_FROM_EMAIL
# SECRET_KEY = ""
# ALLOWED_HOSTS = [".itugnu.org"]
TIME_ZONE = "Europe/Istanbul"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'testdb',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

RAVEN_CONFIG = {
    'dsn': '',
    'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}
