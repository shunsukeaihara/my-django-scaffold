# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.core import signing
from django.core.signing import BadSignature, SignatureExpired

from .settings import api_settings

UserModel = get_user_model()

TOKEN_EMAIL_CONFIRM = "confirm"
TOKEN_ACTIVATION = "activation"
TOKEN_PASSWORD_RESET = "reset"


def create_token(user, type, compress=True):
    return signing.dumps({"u": user.id, "type": type}, compress=compress)


def check_type(obj, type):
    if "type" in obj and obj["type"] == type:
        return True
    else:
        return False


def verify_token(token, type, max_age):
    # BadSignatureかSinatureExpiredが例外として返される
    # それ以外は、userの情報が無い、userが存在しない場合はNoneを返し、いる場合はuserを返す
    try:
        obj = signing.loads(token, max_age=max_age)
        if not check_type(obj, type):
            raise BadSignature()
    except BadSignature as e:
        # 404
        raise e
    except SignatureExpired as e:
        # 410
        raise e
    if 'u' not in obj:
        # 401 bad request
        return None
    return UserModel.objects.filter(pk=obj['u']).first()


def create_email_confirm_token(user):
    return create_token(user, TOKEN_EMAIL_CONFIRM)


def verify_email_confirm_token(user, max_age):
    return verify_token(user, TOKEN_EMAIL_CONFIRM, max_age)


def create_activation_token(user):
    return create_token(user, TOKEN_ACTIVATION)


def verify_activation_token(user, max_age):
    return verify_token(user, TOKEN_ACTIVATION, max_age)


def create_password_reset_token(user):
    return create_token(user, TOKEN_PASSWORD_RESET)


def verify_password_reset_token(user, max_age):
    return verify_token(user, TOKEN_PASSWORD_RESET, max_age)


def create_email_confirmation_url(token):
    return (api_settings.SITE_DOMAIN + api_settings.EMAIL_CONFIRMATION_PATH_TEMPLATE).format(token=token)


def create_password_reset_url(token):
    return (api_settings.SITE_DOMAIN + api_settings.PASSWORD_RESET_PATH_TEMPLATE).format(token=token)


def create_activation_url(token):
    return (api_settings.SITE_DOMAIN + api_settings.ACTIVATION_PATH_TEMPLATE).format(token=token)
