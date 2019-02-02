# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.core import signing
from django.core.signing import BadSignature, SignatureExpired

from .settings import api_settings


TOKEN_EMAIL_CONFIRM = "confirm"
TOKEN_EMAIL_CHANGE = "change"
TOKEN_ACTIVATION = "activation"
TOKEN_PASSWORD_RESET = "reset"


def create_token(user, type, compress=True):
    return signing.dumps({"u": user.id, "type": type}, compress=compress)


def create_email_token(user, email, type, compress=True):
    return signing.dumps({"u": user.id, "email": email, "type": type}, compress=compress)


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
    except SignatureExpired as e:
        # 410
        print(e)
        raise e
    except BadSignature as e:
        # 404
        raise e
    if 'u' not in obj:
        # 401 bad request
        return None
    return get_user_model().objects.filter(pk=obj['u']).first()


def verify_email_token(token, type, max_age):
    # BadSignatureかSinatureExpiredが例外として返される
    # それ以外は、userの情報が無い、userが存在しない場合はNoneを返し、いる場合はuserを返す
    try:
        obj = signing.loads(token, max_age=max_age)
        if not check_type(obj, type):
            raise BadSignature()
    except SignatureExpired as e:
        # 410
        print(e)
        raise e
    except BadSignature as e:
        # 404
        raise e
    if 'u' not in obj:
        # 401 bad request
        return None
    if 'email' not in obj:
        # 401 bad request
        return None
    return get_user_model().objects.filter(pk=obj['u']).first(), obj['email']


def get_user_and_tokentype(token):
    try:
        obj = signing.loads(token)
        if "type" not in obj or "u" not in obj:
            raise BadSignature()
    except BadSignature as e:
        # signatureが壊れてる
        raise e
    return get_user_model().objects.filter(pk=obj['u']).first(), obj["type"]


def get_email_from_token(token):
    try:
        obj = signing.loads(token)
        if "type" not in obj or "u" not in obj or "email" not in obj:
            raise BadSignature()
    except BadSignature as e:
        # signatureが壊れてる
        raise e
    return obj["email"]


def create_email_confirm_token(user):
    return create_token(user, TOKEN_EMAIL_CONFIRM)


def verify_email_confirm_token(token, max_age):
    return verify_token(token, TOKEN_EMAIL_CONFIRM, max_age)


def create_email_change_token(user, email):
    return create_email_token(user, email, TOKEN_EMAIL_CHANGE)


def verify_email_change_token(token, max_age):
    return verify_email_token(token, TOKEN_EMAIL_CHANGE, max_age)


def create_activation_token(user):
    return create_token(user, TOKEN_ACTIVATION)


def verify_activation_token(token, max_age):
    return verify_token(token, TOKEN_ACTIVATION, max_age)


def create_password_reset_token(user):
    return create_token(user, TOKEN_PASSWORD_RESET)


def verify_password_reset_token(token, max_age):
    return verify_token(token, TOKEN_PASSWORD_RESET, max_age)


def create_email_confirmation_url(token):
    return (api_settings.FRONTEND_DOMAIN_WITH_SCHEME + api_settings.EMAIL_CONFIRMATION_PATH_TEMPLATE)\
        .format(token=token)


def create_email_change_url(token):
    return (api_settings.FRONTEND_DOMAIN_WITH_SCHEME + api_settings.EMAIL_CHANGE_PATH_TEMPLATE)\
        .format(token=token)


def create_password_reset_url(token):
    return (api_settings.FRONTEND_DOMAIN_WITH_SCHEME + api_settings.PASSWORD_RESET_PATH_TEMPLATE).format(token=token)


def create_activation_url(token):
    return (api_settings.FRONTEND_DOMAIN_WITH_SCHEME + api_settings.ACTIVATION_PATH_TEMPLATE).format(token=token)
