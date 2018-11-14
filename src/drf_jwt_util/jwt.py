# -*- coding: utf-8 -*-
from datetime import datetime
from calendar import timegm
from rest_framework_jwt.settings import api_settings as jwt_api_settings

from .settings import api_settings


def jwt_get_username_from_payload_handler(payload):
    return payload['uid']


def jwt_payload_handler(user):
    # store only user_id in the payload
    payload = {
        'uid': user.id,
        'exp': datetime.utcnow() + jwt_api_settings.JWT_EXPIRATION_DELTA
    }
    if jwt_api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(datetime.utcnow().utctimetuple())
    if jwt_api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = jwt_api_settings.JWT_AUDIENCE

    if jwt_api_settings.JWT_ISSUER is not None:
        payload['iss'] = jwt_api_settings.JWT_ISSUER
    return payload


def jwt_response_payload_handler(token, user=None, request=None):
    UserSerializer = api_settings.USER_SERIALIZER
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }
