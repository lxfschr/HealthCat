"""
Django settings for healthcat_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd9v#^ou*ky8z06ydf7mk!dcy7dvt9adtu!+gm0_hnj%()_p6u+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TIME_INPUT_FORMATS = ('%H:%M', '%I:%M%p', '%I:%M %p')
DATE_FORMAT = '%m/%d/%y'
DATETIME_FORMAT = '%I:%M%p %m/%d/%y'

# Application definition
DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.formtools', # form wizard
)

# Apps that needed to be pip installed.
THIRD_PARTY_APPS = (
    'django_nvd3',
)

# Apps that we create, like healthcat.
LOCAL_APPS = (
    'healthcat',
)

# Put it all together for Django.
INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'healthcat_project.urls'

# Used by the authentication system for the healthcat application.
# URL to use if the authentication system requires a user to log in.
LOGIN_URL = '/healthcat/login'

# Default URL to redirect to after a user logs in.
LOGIN_REDIRECT_URL = '/healthcat/'

WSGI_APPLICATION = 'healthcat_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static asset configuration
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# Configures Django to merely print emails rather than sending them.
# Comment out this line to enable real email-sending.
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# To enable real email-sending, you should uncomment and 
# configure the settings below.
EMAIL_HOST = 'smtp.gmail.com'               # perhaps 'smtp.andrew.cmu.edu'
EMAIL_HOST_USER = 'healthcat.info@gmail.com'      # perhaps your Andrew ID
EMAIL_HOST_PASSWORD = 'webapps15637'
EMAIL_USE_TLS = True
EMAIL_PORT = 587

# EMAIL_HOST_USER = 'healthcat15637@gmail.com' 

# Parse database configuration from $DATABASE_URL
import dj_database_url

# UNCOMMENT FOR HEROKU DEPLOYMENT #
#DATABASES['default'] =  dj_database_url.config() 

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

COLORS = ["225B66", "17A3A5", "8DBF67", "FCCB5F", "FC6E59", "FC90E6"]
NEXT_COLOR = COLORS[0]