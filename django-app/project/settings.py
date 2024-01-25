import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-83hec8q_rze@^t8)wdgpl46undbym_=+%ntzwfdok&(26cm=z2"

DEBUG = True

ALLOWED_HOSTS = []

CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000", "http://localhost:8000"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "testing",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES_DIR = BASE_DIR / "templates"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "ru"

# LANGUAGES = [
#     ('ru', _('Русский')),
#     ('en', _('English')),
# ]

TIME_ZONE = "Asia/Yekaterinburg"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOGIN_URL = "login"
LOGOUT_URL = "logout"
LOGOUT_REDIRECT_URL = "logout"
LOGIN_REDIRECT_URL = "testing:home"
