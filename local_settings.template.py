from itugnu.base import INSTALLED_APPS, MIDDLEWARE  # NOQA

DEBUG = False
DEBUG_TOOLBAR = False

# Email Settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = ""
EMAIL_PORT = 465
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = ""
DEFAULT_CONTACT_EMAIL = DEFAULT_FROM_EMAIL
SECRET_KEY = ""
ALLOWED_HOSTS = [".itugnu.org"]
TIME_ZONE = "Europe/Istanbul"
