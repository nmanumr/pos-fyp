import os

from xmodule import env


def configure_db(settings):
    settings['DATABASES'] = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',

            'NAME': env.get('POSTGRES_DB_NAME', 'pos'),
            'USER': env.get('POSTGRES_USERNAME', 'postgres'),
            'PASSWORD': env.get('POSTGRES_PASSWORD', ''),

            'HOST': env.get('POSTGRES_HOSTNAME', 'localhost'),
            'PORT': env.get_int('POSTGRES_PORT', 5432),
        }
    }
