"""
Django settings for portafolio project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ul$&4-qpl76@d4xi&e2%=^az&c#$cr1=(10b_$*=t%q-=+spt^'

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
    'ecommerse',
<<<<<<< HEAD
    'widget_tweaks'
=======
>>>>>>> 02e8b3697dcc47d645419c7bd46c834e358461b4
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

ROOT_URLCONF = 'portafolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
<<<<<<< HEAD
        'DIRS': [BASE_DIR / 'templates'],
=======
        'DIRS': [],
>>>>>>> 02e8b3697dcc47d645419c7bd46c834e358461b4
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ecommerse.context_processor.total_carrito',
            ],
        },
    },
]

WSGI_APPLICATION = 'portafolio.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mpagency',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'Localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

<<<<<<< HEAD
LANGUAGE_CODE = 'es'
=======
LANGUAGE_CODE = 'en-us'
>>>>>>> 02e8b3697dcc47d645419c7bd46c834e358461b4

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
<<<<<<< HEAD
STATICFILES_DIRS = [BASE_DIR / 'ecommerse' / 'static']
=======
>>>>>>> 02e8b3697dcc47d645419c7bd46c834e358461b4

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# settings.py
AUTH_USER_MODEL = 'ecommerse.Usuario'
# settings.py

<<<<<<< HEAD
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # Se define el backend que utilizara django para enviar correos, El SMTP (Simple Mail Transfer Protocol) es el protocolo estándar para enviar correos electrónicos.
EMAIL_HOST = 'smtp-relay.brevo.com'  # SMTP server de Brevo, este sera el servicio de correo electronico 
EMAIL_PORT = 587  # Puerto 587 es para TLS (Transport Layer Security), protocolo de cifrado que asegura la comunicación entre la aplicación y el servidor de correo.
EMAIL_USE_TLS = True  # Activar TLS
EMAIL_HOST_USER = 'bastianmadrid72@gmail.com'  # correo registrado en Brevo, este corre envia los email al usuario que quiera cambiar la contraseña
=======
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'  # SMTP server de Brevo
EMAIL_PORT = 587  # Puerto 587 es para TLS
EMAIL_USE_TLS = True  # Activar TLS
EMAIL_HOST_USER = 'bastianmadrid72@gmail.com'  # Tu correo registrado en Brevo (como aparece en la imagen)
>>>>>>> 02e8b3697dcc47d645419c7bd46c834e358461b4
EMAIL_HOST_PASSWORD = 'B19hYzSrVXqcjdD3'  # La clave SMTP que generaste en Brevo
DEFAULT_FROM_EMAIL = 'bastianmadrid72@gmail.com'  # Dirección de remitente por defecto

#______

LOGIN_URL = '/inicio_sesion/'

<<<<<<< HEAD
#______

# Para mostrar las imagenes en mi carrito
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
=======
#______
>>>>>>> 02e8b3697dcc47d645419c7bd46c834e358461b4
