from django.conf import settings
from rest_framework.settings import APISettings


USER_SETTINGS = getattr(settings, 'DRF_JWT_UTIL', None)

DEFAULTS = {
    'REQUIRE_EMAIL_CONFIRMATION': False,
    "FRONTEND_DOMAIN_WITH_SCHEME": "http://127.0.0.1:3000",
    "PASSWORD_RESET_PATH_TEMPLATE": "/reset/{token}",
    "ACTIVATION_PATH_TEMPLATE": "/activate/{token}",
    "EMAIL_CONFIRMATION_PATH_TEMPLATE": "/confirm/{token}",
    "EMAIL_CHANGE_PATH_TEMPLATE": "/emailchange/{token}",
    "USER_SERIALIZER": "drf_jwt_util.serializers.DefaultUserSerializer",
    "ACTIVATION_SERIALIZER": "drf_jwt_util.serializers.PasswordSerializer",
    "FROM_EMAIL": settings.DEFAULT_FROM_EMAIL,
}


IMPORT_STRINGS = [
    "USER_SERIALIZER",
    "ACTIVATION_SERIALIZER",
]

api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)
