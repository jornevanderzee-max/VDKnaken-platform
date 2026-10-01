"""
Instellingen voor het VDK Arbeidsvoorwaardenplatform.

Alles wat per omgeving verschilt (ontwikkelen, test, productie) komt uit
omgevingsvariabelen. In de Codespace staan die in
`.devcontainer/docker-compose.yml`. Zet hier nooit geheimen neer.
"""

import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent


def lijst_uit_omgeving(naam):
    """Leest een kommagescheiden omgevingsvariabele als lijst."""
    return [deel.strip() for deel in os.environ.get(naam, "").split(",") if deel.strip()]


DEBUG = os.environ.get("DJANGO_DEBUG") == "1"

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise ImproperlyConfigured("De omgevingsvariabele DJANGO_SECRET_KEY ontbreekt.")

ALLOWED_HOSTS = lijst_uit_omgeving("DJANGO_ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = lijst_uit_omgeving("DJANGO_CSRF_TRUSTED_ORIGINS")


# Onderdelen van de applicatie

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Eigen apps, zie docs/plan.md
    "accounts",
    "catalogus",
    "bedrijven",
    "publiek",
    "portaal",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database: altijd PostgreSQL, via DATABASE_URL

DATABASES = {
    "default": dj_database_url.config(env="DATABASE_URL", conn_max_age=600),
}
if not DATABASES["default"]:
    raise ImproperlyConfigured("De omgevingsvariabele DATABASE_URL ontbreekt.")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Gebruikers en wachtwoorden

AUTH_USER_MODEL = "accounts.Gebruiker"

# Argon2 voor nieuwe wachtwoorden; de rest alleen om oude hashes te kunnen lezen.
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 10}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Taal en tijd: teksten in de code zijn Engels, de Nederlandse vertaling staat in locale/nl/.

LANGUAGE_CODE = "nl"
LANGUAGES = [
    ("nl", _("Dutch")),
]
LOCALE_PATHS = [BASE_DIR / "locale"]
USE_I18N = True

TIME_ZONE = "Europe/Amsterdam"
USE_TZ = True


# Statische bestanden (CSS, JavaScript in static/vendor/)

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"


# Mail: in de Codespace gaat alles naar Mailpit (poort 8025)

EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "25"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS") == "1"
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@localhost")


# Beveiliging buiten ontwikkeling

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 365
    SECURE_CONTENT_TYPE_NOSNIFF = True
