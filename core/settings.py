import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',')

DJANGO_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'whitenoise.runserver_nostatic',
]

CALENDAR_APPS = [
    'accounts',
    'events',
    'lodge',
    'setup',
    'calendarrequest',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CALENDAR_APPS

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = [
    'https://sistema.agendamaconica.site',
]

JAZZMIN_SETTINGS = {
    "site_title": "Calendário de Eventos",
    "site_header": "Calendário de Eventos",
    "site_brand": "Calendário de Eventos",
    "site_logo": "core/imgs/maconaria.webp",
    "show_sidebar": True,
    "custom_css": "core/css/custon_jazzmin.css",
    "navigation_expanded": True,
    "site_icon": None,
    "login_logo": None,
    "welcome_sign": "Calendário de Eventos",
    "topmenu_links": [
        {"model": "auth.User"},
        {"model": "setup.Setup"},
        {"model": "lodge.Lodge"},
        {"model": "accounts.Brother"},
        {"model": "events.Event"},
        {"model": "calendarrequest.StoreRequest"},
        {"model": "calendarrequest.EventRequest"},
        {"model": "calendarrequest.CancelEventRequest"},
    ],

    "order_with_respect_to": [
        "auth.User",
        "auth.Group",
        "setup.Setup",
        "lodge.Lodge",
        "accounts.Brother",
        "events.Event",
        "calendarrequest.StoreRequest",
        "calendarrequest.EventRequest",
        "calendarrequest.CancelEventRequest",
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "accounts.CustomUser": "fas fa-user",
        "calendarrequest.UserRequest": "fas fa-user",
        "auth.Group": "fas fa-users",
        "accounts.Brother": "fas fa-users",
        "setup.Setup": "fas fa-cogs",
        "events.Event": "fas fa-calendar-alt",
        "lodge.Lodge": "fas fa-home",
        "calendarrequest.StoreRequest": "fas fa-home",
        "calendarrequest.EventRequest": "fas fa-calendar-alt",
        "calendarrequest.CancelEventRequest": "fas fa-calendar-times",
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGIN_URL = '/admin/'

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'core' / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Logging configurado para console
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} | {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'accounts': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'events': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'solicitacoes': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

AUTH_USER_MODEL = 'accounts.CustomUser'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.hostinger.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_HOST_USER = 'sistema@agendamaconica.site'
EMAIL_HOST_PASSWORD = '@gendamaconicA123'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_TIMEOUT = 30
# ADMIN_EMAIL = EMAIL_HOST_USER
# ADMIN_EMAIL = "fernandovalentedev@gmail.com"

# Configuração do WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
