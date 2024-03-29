"""
Django settings for ISIS4426_Grupo06_Proyecto1 project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h+$c+z=y+8!i&9has5+mij578@2bqsutp1x@fqpe^$z3^%y&+i'

# NOTE 1: CHANGE to DEBUG = False 
DEBUG = True

# NOTE 2: CHANGE TO ALLOWED_HOSTS = ['*'] 
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom Apps

    'users',
    'designs',

    # Support to S3

    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ISIS4426_Grupo06_Proyecto1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
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

WSGI_APPLICATION = 'ISIS4426_Grupo06_Proyecto1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# NOTE 3: Postgres database

# Comment to MONGO databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'Proyecto1',
#        'USER': 'postgres',
#        'PASSWORD': 'Dsa123',
#        'HOST': '127.0.0.1',
#        'PORT' : '5432'
#    }
#}

# NOTE 4: Mongo databse

# Comment to POSTGRES databases

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'proyecto1',
        'HOST': '18.210.47.72',
    }
}   

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://webservercache.mwhg6v.0001.use1.cache.amazonaws.com",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "cachesesion"
    },
    'session': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://webservercache.mwhg6v.0001.use1.cache.amazonaws.com',
        'OPTIONS': {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
    }
}

CACHE_TTL = 60 * 15
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'session'
# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, 'static'),
#)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

LOGIN_URL = '/users/login/'

#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#MEDIA_URL = '/media/'

# SQS queue configuration
APP_AWS_QUEUE = {
  'region_name': 'us-east-1',
  'aws_access_key_id': 'AKIAWMDWJXRQEMTXLLHF',
  'aws_secret_access_key': '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',
  'sqs_queue_url': 'https://sqs.us-east-1.amazonaws.com/438334766176/queuse_design_std'
}

# S3
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

# Static
#AWS_LOCATION = 'static'
#STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
#STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Media
#PUBLIC_MEDIA_LOCATION = ''
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
