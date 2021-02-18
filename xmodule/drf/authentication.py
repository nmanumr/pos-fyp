from django.apps import apps as django_apps
from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed


class AccessTokenAuthentication(BaseAuthentication):
    keyword = 'AccessToken'
    model = django_apps.get_model(settings.ACCESS_TOKEN_MODEL, require_ready=False)

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return

        if len(auth) == 1:
            raise AuthenticationFailed('Invalid token header. No credentials provided.')

        elif len(auth) > 2:
            raise AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            token = auth[1].decode()
        except UnicodeError:
            raise AuthenticationFailed('Invalid token header. Token string should not contain invalid characters.')

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.select_related('user').get(access_token=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if token.is_expired:
            raise AuthenticationFailed(
                'Authentication token expired. Please refresh your token.',
                code='token_expired'
            )

        token.last_accessed = timezone.now()
        token.save(update_fields=['last_accessed'])

        user = token.user
        if not user.is_active:
            raise AuthenticationFailed(
                'User inactive or deleted.',
                code='inactive_user'
            )

        return user, token

    def authenticate_header(self, request):
        return self.keyword
