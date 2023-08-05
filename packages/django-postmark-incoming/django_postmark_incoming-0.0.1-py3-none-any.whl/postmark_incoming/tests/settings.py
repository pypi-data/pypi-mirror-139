import os
import os.path

BASE_DIR = os.path.dirname(__file__)
DEBUG = False
SECRET_KEY = "not a real secret"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "postmark_incoming",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "postmark_incoming.tests.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}

TIME_ZONE = "UTC"
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Celery - Will only be used if you pip install celery
# https://docs.celeryproject.org/en/stable/getting-started/brokers/redis.html
CELERY_BROKER_URL = None
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_TIME_LIMIT = 60  # Raise exception after 60 seconds.
CELERY_WORKER_TASK_LOG_FORMAT = "[%(name)s] at=%(levelname)s timestamp=%(asctime)s processName=%(processName)s task_id=%(task_id)s task_name=%(task_name)s %(message)s"
CELERY_WORKER_LOG_FORMAT = "[%(name)s] at=%(levelname)s timestamp=%(asctime)s processName=%(processName)s %(message)s"
CELERY_WORKER_LOG_COLOR = False
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
