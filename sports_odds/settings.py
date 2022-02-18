import os
from pathlib import Path

import dj_database_url
from decouple import config, Csv

USE_DOCKER = config('DOCKER', default=True, cast=bool)
if USE_DOCKER:
    # For the docker
    # on docker container, we will map backend dir to /home/user/app/ and BASE_DIR will be set to </home/user/app/>
    BASE_DIR = '/home/user/'
    BACKEND_DIR = '/home/user/app/'
    FRONTEND_DIR = '/home/user/frontend'
else:
    # For the local test
    # While testing on local, this will be the root folder (where readme.md is)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # this will be <root>
    BACKEND_DIR = BASE_DIR
    # this will be <root>/frontend/
    FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')


SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# cors setting
CORS_ORIGIN_ALLOW_ALL = True
CORS_PREFLIGHT_MAX_AGE = 3000

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
            FRONTEND_DIR
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
<<<<<<< HEAD
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
=======
     'default': dj_database_url.config(
        default=config('DATABASE_URL')
    ),
>>>>>>> e0c7a0f4c34a52158d4796706cc707c4e538600c
}

# async setting
DJANGO_ALLOW_ASYNC_UNSAFE = True 

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
LANGUAGE_CODE = 'en-us'

USE_TZ = True
TIME_ZONE = 'Etc/UTC'

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
CSS_URL = '/css/'

if USE_DOCKER:
    # for docker
    STATICFILES_DIRS = [
        os.path.join(BACKEND_DIR, 'static')
        # os.path.join(FRONTEND_DIR, 'static')
    ]
    STATIC_ROOT = '/home/user/staticfiles'
    MEDIA_ROOT = os.path.join(FRONTEND_DIR, 'media')
    CSS_ROOT = os.path.join(FRONTEND_DIR, 'css')
else:
    STATICFILES_DIRS = [
        # for local test use the following two
        os.path.join(FRONTEND_DIR, 'build'),
        os.path.join(FRONTEND_DIR, 'build', 'static')
    ]

    # for local test we make staticfiles dir on the root
    STATIC_ROOT = os.path.join(BACKEND_DIR, 'static')
    MEDIA_ROOT = os.path.join(FRONTEND_DIR, 'build', 'media')
    CSS_ROOT = os.path.join(FRONTEND_DIR, 'build', 'css')

# Channels
ASGI_APPLICATION = 'sports_odds.routing.application'

APPEND_SLASH = False

CHANNEL_LAYERS = {
     'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [config('CHANNEL_HOST', default='redis://localhost:6379')],
            "capacity": 1500,  # default 100
            "expiry": 10,  # default 60
        },
    },
}

# celery settings
# redis
REDIS_URL = config('REDIS_URL')

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
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERYD_PREFETCH_MULTIPLIER = 0

from .logger import LOGGING

#AUTH_USER_MODEL = 'backend.User'

SITE_ID = 1

FILE_UPLOAD_MAX_MEMORY_SIZE = 5368709120
DATA_UPLOAD_MAX_MEMORY_SIZE = 5368709120

# Setup support for proxy headers
# https://stackoverflow.com/questions/58013545/how-change-schemes-from-http-to-https-in-drf-yasg
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

