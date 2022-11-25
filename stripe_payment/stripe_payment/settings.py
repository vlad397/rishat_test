import os
from urllib.parse import urljoin

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = str(os.getenv('SECRET_KEY'))
STRIPE_PUBLISHABLE_KEY = str(os.getenv('STRIPE_PUBLISHABLE_KEY'))
STRIPE_SECRET_KEY = str(os.getenv('STRIPE_SECRET_KEY'))

ORDER_SESSION_ID = 'order'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:80/')
SUCCESS_BASE_LINK = os.getenv('SUCCESS_BASE_LINK', 'success/')
CANCEL_BASE_LINK = os.getenv('CANCEL_BASE_LINK', 'cancel/')
SUCCESS_LINK = urljoin(BASE_URL, SUCCESS_BASE_LINK)
CANCEL_LINK = urljoin(BASE_URL, CANCEL_BASE_LINK)


DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',
    'testserver',
    'backend',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'rest_framework',
    'api'
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


ROOT_URLCONF = 'stripe_payment.urls'


WSGI_APPLICATION = 'stripe_payment.wsgi.application'


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

include(
    "components/database.py",
    "components/templates.py",
)
