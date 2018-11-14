from django.conf import settings
from rest_framework.settings import APISettings


USER_SETTINGS = getattr(settings, 'DRF_JWT_UTIL', None)

DEFAULTS = {
    'REQUIRE_EMAIL_CONFIRMATION': False,
    "SITE_DOMAIN": "http://127.0.0.1:8000",
    "PASSWORD_RESET_PATH_TEMPLATE": "/password_reset/{token}",
    "ACTIVATION_PATH_TEMPLATE": "/activate/{token}",
    "EMAIL_CONFIRMATION_PATH_TEMPLATE": "/confirmation/{token}",
    "USER_SERIALIZER": "drf_jwt_util.serializers.DefaultUserSerializer",
    "FROM_EMAIL": "webmaster@localhost",
}


IMPORT_STRINGS = [
    "USER_SERIALIZER"
]

api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)
