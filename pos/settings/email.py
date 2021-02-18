def configure_email(settings):
    if settings['DEBUG']:
        settings['EMAIL_BACKEND'] = 'django.core.mail.backends.filebased.EmailBackend'
        settings['EMAIL_FILE_PATH'] = '/tmp/emails/'
    else:
        # TODO: Configure email for production
        pass
