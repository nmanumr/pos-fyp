INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

ACCESS_TOKEN_MODEL = 'accounts.UserAccessToken'

ACCOUNTS_EMAIL_VERIFICATION_EXPIRE_DAYS = 3
ACCOUNTS_MIN_USERNAME_LENGTH = 5
