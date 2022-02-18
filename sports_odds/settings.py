"""
Django settings for sports_odds project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

###
# Production settings
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wnzzrmtypcwe(37jn)kc7ec(917clw!7@vf=_3w7=@c(3zk^m-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

###

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*', '192.168.1.108']

CORS_ORIGIN_ALLOW_ALL = True
# Application definition

INSTALLED_APPS = [
    'api.apps.AppConfig',
    'channels',
    'django_celery_beat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # third party packages
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'django_filters',


    # swagger ui documentation generator
    'drf_yasg',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASS': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.PageNumberPaginationWithCount',
    'PAGE_SIZE': 20,
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sports_odds.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # BASE_DIR / './../frontend/build'
        ],
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

WSGI_APPLICATION = 'sports_odds.wsgi.application'


SWAGGER_SETTINGS = {
    'DEFAULT_PAGINATOR_INSPECTORS': [
        'api.inspector.PageNumberPaginationWithCountInspector',
        'drf_yasg.inspectors.DjangoRestResponsePagination',
        'drf_yasg.inspectors.CoreAPICompatInspector',
    ],
    'SECURITY_DEFINITIONS': None,
    # {
    #     'basic': {
    #         'type': 'basic'
    #     }
    #     # 'Token': {
    #     #     'type': 'apiKey',
    #     #     'name': 'Authorization',
    #     #     'in': 'header'
    #     # }
    # },
    'OPERATIONS_SORTER': None,
    'REQUIRED_PROPS_FIRST': True,
}

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_sports_odds',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_TZ = True
TIME_ZONE = 'Etc/UTC'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    BASE_DIR / '../web_backend/api/static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CSS_URL = '/css/'
CSS_ROOT = BASE_DIR / 'css'

LOGIN_URL = '/login/'


# Channels
ASGI_APPLICATION = 'sports_odds.routing.application'

APPEND_SLASH = False

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# celery settings
# redis
REDIS_URL = 'redis://localhost:6379/1'

# Celery
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACKS_LATE = True
BROKER_URL = REDIS_URL
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_TIMEZONE = 'UTC'

from .logger import LOGGING
#AUTH_USER_MODEL = 'backend.User'

SITE_ID = 1

FILE_UPLOAD_MAX_MEMORY_SIZE = 5368709120
DATA_UPLOAD_MAX_MEMORY_SIZE = 5368709120
