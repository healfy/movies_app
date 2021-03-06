"""
Django settings for movies_app project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sw8*(2cny^ak62nz=@qa)zxfuc0mlk&^og&gx)kl3j1e$c2($='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'video_encoding',
    'movies',
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

ROOT_URLCONF = 'movies_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'movies_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('PGDATABASE') or 'mybb',
        'USER': os.getenv('PGUSER') or 'mybb',
        'PASSWORD':  os.getenv('PGPASSWORD') or 'changeme',
        'HOST': os.getenv('PGHOST') or '0.0.0.0',
        'PORT': os.getenv('PGPORT') or '3307',
        'OPTIONS': {
            'init_command': 'SET '
                'storage_engine=INNODB,'
                'character_set_server=utf8,'
                'collation_server=utf8_unicode_ci',
        }
    }
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ]
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/tmp/movies-static'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

WIDTH = 640
HEIGHT = 360

VIDEO_ENCODING_FORMATS = {
    'FFmpeg': [
        {
            'name': 'webm_sd',
            'extension': 'webm',
            'params': [
                '-b:v', '1000k', '-maxrate', '1000k', '-bufsize', '2000k',
                '-codec:v', 'libvpx', '-r', '30',
                '-vf', f'scale={WIDTH}x{HEIGHT}', '-qmin', '10', '-qmax', '42',
                '-codec:a', 'libvorbis', '-b:a', '128k', '-f', 'webm',
            ],
        },
        {
            'name': 'mp4_sd',
            'extension': 'mp4',
            'params': [
                '-codec:v', 'libx264', '-crf', '20', '-preset', 'medium',
                '-b:v', '1000k', '-maxrate', '1000k', '-bufsize', '2000k',
                '-vf', f'scale={WIDTH}x{HEIGHT}',  # http://superuser.com/a/776254
                '-codec:a', 'aac', '-b:a', '128k', '-strict', '-2',
            ],
        },
    ]
}

VIDEO_ENCODING_THREADS = 4

MAZ_VIDEO_SIZE = 2e8  # 200 mb approx

import sys
sys.path.append('/etc/movies_app')

for path in (BASE_DIR, '/etc/movies_app'):
    if os.path.exists(os.path.join(path, 'local_settings.py')):
        from local_settings import *

if os.path.exists('movies_app/local_settings.py'):
    from movies_app.local_settings import *
