from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _


class JWTAuthentication(JSONWebTokenAuthentication):
    def authenticate_credentials(self, payload):
        user = self.get_user_from_payload(payload)
        return user

    def get_user_from_payload(self, payload):
        User = get_user_model()
        try:
            user = User.objects.get(pk=payload.get('uid'))
        except User.DoesNotExist:
            msg = _('Invalid signature.')
            raise exceptions.AuthenticationFailed(msg)
        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.AuthenticationFailed(msg)
        return user
