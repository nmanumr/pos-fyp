REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'xmodule.drf.renderers.CamelCaseJSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'xmodule.drf.parsers.CamelCaseJSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'xmodule.drf.authentication.AccessTokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'xmodule.drf.permissions.IsVerified',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 25
}


def configure_drf(settings):
    if settings['DEBUG']:
        # Render API response as Browsable API Response in development environment
        REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += (
            'rest_framework.renderers.BrowsableAPIRenderer',
        )
