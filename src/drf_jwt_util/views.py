# -*- coding: utf-8 -*-
import datetime
from django.core.signing import BadSignature, SignatureExpired
from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import NotFound, APIException
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings as jwt_api_settings
from rest_framework_jwt.views import RefreshJSONWebToken, ObtainJSONWebToken

from .email import send_confirmation_email
from .serializers import RegisterSerializer, PasswordSerializer
from .serializers import RefreshJSONWebTokenSerializer, ObtainJSONWebTokenSerializer
from .settings import api_settings
from .signing import verify_email_confirm_token, create_email_confirm_token
from .signing import verify_activation_token, verify_password_reset_token


jwt_payload_handler = jwt_api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = jwt_api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = jwt_api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
refresh_jwt_token = RefreshJSONWebToken.as_view(serializer_class=RefreshJSONWebTokenSerializer)
obtain_jwt_token = ObtainJSONWebToken.as_view(serializer_class=ObtainJSONWebTokenSerializer)


def create_jwt_response(request, user, statuscode=status.HTTP_201_CREATED):
    token = jwt_encode_handler(jwt_payload_handler(user))
    res = jwt_response_payload_handler(token, user, request)
    return Response(res, status=statuscode)


class RegisterView(GenericAPIView):
    """
    emailとpasswordを指定してユーザ登録
    """
    serializer_class = RegisterSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        # email confirmationが必要ならis_activeをfalseで作成する
        user = s.save(is_active=not(api_settings.REQUIRE_EMAIL_CONFIRMATION))
        if api_settings.REQUIRE_EMAIL_CONFIRMATION:
            # ToDo: send confirm email
            token = create_email_confirm_token(user)
            send_confirmation_email(user, token)
            return Response()
        response = create_jwt_response(request, user)
        if jwt_api_settings.JWT_AUTH_COOKIE:
            expiration = (datetime.utcnow() + jwt_api_settings.JWT_EXPIRATION_DELTA)
            response.set_cookie(jwt_api_settings.JWT_AUTH_COOKIE,
                                token,
                                expires=expiration,
                                httponly=True)
        return response


class EmailConfirmView(GenericAPIView):
    """
    emailの存在チェックをするview
    これを通らないとuserがactiveにならない->作成時にis_activeをfalseにするとかする
    """
    def verify_token(self, token):
        try:
            user = verify_email_confirm_token(token, datetime.timedelta(hours=24))
            if user is None:
                raise NotFound()
            return user
        except BadSignature:
            raise NotFound()
        except SignatureExpired:
            raise APIException(detail="", code=status.HTTP_410_GONE)

    def get(self, request, token):
        self.verify_token(token)
        return Response()  # emailも返す?

    def post(self, request, token):
        user = self.verify_token(token)
        user.is_active = True
        user.save()
        return create_jwt_response(request, user, statuscode=status.HTTP_200_OK)


class ActivationView(GenericAPIView):
    """
    userが他社によって登録されたので、パスワードを設定してactivationする
    """
    serializer_class = PasswordSerializer

    def verify_token(self, token):
        try:
            user = verify_activation_token(token, datetime.timedelta(hours=24))
            if user is None:
                raise NotFound()
            return user
        except BadSignature:
            raise NotFound()
        except SignatureExpired:
            raise APIException(detail="", code=status.HTTP_410_GONE)

    def get(self, request, token):
        self.verify_token(token)
        return Response()  # emailも返す?

    def post(self, request, token):
        user = self.verify_token(token)
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        user.is_active = True
        user.set_password(s.password)
        user.save()
        return create_jwt_response(request, user, statuscode=status.HTTP_200_OK)


class PasswordResetView(GenericAPIView):
    serializer_class = PasswordSerializer

    def verify_token(self, token):
        try:
            user = verify_password_reset_token(token, datetime.timedelta(hours=24))
            if user is None:
                raise NotFound()
            return user
        except BadSignature:
            raise NotFound()
        except SignatureExpired:
            raise APIException(detail="", code=status.HTTP_410_GONE)

    def get(self, request, token):
        self.verify_token(token)
        return Response()

    def post(self, request, token):
        user = self.verify_token(token)
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        user.is_active = True
        user.set_password(s.password)
        user.save()
        return Response()  # resetの場合は再度loginさせる方が良い気はする
