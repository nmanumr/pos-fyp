from .apps import *
from .auth import *
from .database import *
from .drf import *
from .email import *
from .host import *
from .logging import *
from .static import *
from .templates import *

DEBUG = env.get_bool('DJANGO_DEBUG', True)
SECRET_KEY = env.get('DJANGO_SECRET_KEY', '<pos-fake-secret-key>')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ENVIRONMENT = env.get('SERVER_ENVIRONMENT')
WSGI_APPLICATION = 'pos.wsgi.application'
ROOT_URLCONF = 'pos.urls'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = env.local_timezone()

# Delayed configuration
settings = locals()
for key in list(settings.keys()):
    if key.startswith('configure_'):
        settings[key](settings)
