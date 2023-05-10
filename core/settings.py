from pathlib import Path
import os
import environ
import dj_database_url

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']

SITE_ID = 1

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    'django_google_maps',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_extensions',

]

OWN_APPS = [
    'accounts',
    'inmuebles',
    'herramientas',
    'payment',
    'enlaces',
    
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + OWN_APPS


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
AUTH_USER_MODEL = "accounts.User"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 3
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT =300
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "account_login"

STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
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


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": 'inmuebles_db',
        "HOST": "localhost",
        "USER": "root",
        "PASSWORD": "",
        "PORT": 3306,
        'OPTIONS': {
        'sql_mode': 'traditional',
        }
    }
}
DATABASES['default']['ATOMIC_REQUESTS'] = True




# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static',]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGOUT_URL = 'account_logout'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#base host
BASE_HOST = env('BASE_HOST')

#configuracion paypal:

SECRET_KEY_PAYPAL = env('SECRET_KEY_PAYPAL')
CLIENT_ID = env('CLIENT_ID')
PAYPAL_API = env('PAYPAL_API')
HEADERS_URL = env('HEADERS_URL')
WEBHOOK_ID = env('WEBHOOK_ID')

#configuracion PayU

MAPS_API_KEY = env('MAPS_API_KEY')

if env('DEBUG'):
    # EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
    CSRF_TRUSTED_ORIGINS  = [
        'http://127.0.0.1:8000',
        'https://127.0.0.1:8000/',
        'http://127.0.0.1:443',
        'https://127.0.0.1:443/',
        'https://d118-189-216-19-11.ngrok-free.app',
    ]
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = env('correo')
    EMAIL_HOST_PASSWORD = env('password')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
else:    
    DATABASES = {
    }
    CSRF_TRUSTED_ORIGINS  = [
        'http://127.0.0.1:8000',
        'https://127.0.0.1:8000/',
        'http://127.0.0.1:443',
        'https://127.0.0.1:443/',
        'https://d118-189-216-19-11.ngrok-free.app',
    ]
    #configuracion smtp del servidor
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = env('correo')
    EMAIL_HOST_PASSWORD = env('password')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
