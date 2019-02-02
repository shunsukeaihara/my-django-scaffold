# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.core.signing import BadSignature, SignatureExpired
from django.db import transaction
from django.utils.translation import ugettext as _
from rest_framework import status
from rest_framework.exceptions import NotFound, APIException
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings as jwt_api_settings
from rest_framework_jwt.views import RefreshJSONWebToken, ObtainJSONWebToken

from .email import send_confirmation_email, resend_email, send_passwordreset_email
from .serializers import RegisterSerializer, PasswordSerializer, EmailSerializer
from .serializers import RefreshJSONWebTokenSerializer, ObtainJSONWebTokenSerializer
from .settings import api_settings
from .signing import (
    verify_email_confirm_token, create_email_confirm_token, create_password_reset_token,
    verify_activation_token, verify_password_reset_token, verify_email_change_token)


jwt_payload_handler = jwt_api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = jwt_api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = jwt_api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
refresh_jwt_token = RefreshJSONWebToken.as_view(serializer_class=RefreshJSONWebTokenSerializer)
obtain_jwt_token = ObtainJSONWebToken.as_view(serializer_class=ObtainJSONWebTokenSerializer)


def create_jwt_response(request, user, statuscode=status.HTTP_201_CREATED):
    token = jwt_encode_handler(jwt_payload_handler(user))
    res = jwt_response_payload_handler(token, user, request)
    return Response(res, status=statuscode)


class TokenExpired(APIException):
    status_code = status.HTTP_410_GONE
    default_detail = _("Token has expired.")


class UserAlreadyConfirmed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("User has already been confirmed.")


class UserAlreadyActivated(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("User has already been activated.")


class UserNotMached(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _("User did not match.")


class RegisterView(GenericAPIView):
    """
    emailとpasswordを指定してユーザ登録
    """
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        # email confirmationが必要ならis_activeをfalseで作成する
        user = s.save(is_active=not(api_settings.REQUIRE_EMAIL_CONFIRMATION))
        if api_settings.REQUIRE_EMAIL_CONFIRMATION:
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


class EmailConfirmView(APIView):
    """
    emailの存在チェックをするview
    これを通らないとuserがactiveにならない->作成時にis_activeをfalseにするとかする
    """
    permission_classes = (AllowAny,)

    def verify_token(self, token):
        try:
            user = verify_email_confirm_token(token, datetime.timedelta(hours=24))
            if user is None:
                raise NotFound()
            if user.is_active:
                raise UserAlreadyConfirmed()
            return user
        except SignatureExpired:
            raise TokenExpired()
        except BadSignature:
            raise NotFound()

    def get(self, request, token):
        self.verify_token(token)
        return Response()  # emailも返す?

    def post(self, request, token):
        user = self.verify_token(token)
        user.is_active = True
        user.save()
        return create_jwt_response(request, user, statuscode=status.HTTP_200_OK)


class EmailChangeConfirmView(APIView):
    """
    新しいemailの存在チェックをするview
    これがアクセスされないとユーザのemailを変更しない
    ToDo: 保存時に既にemailが衝突している場合は対応しない
    """

    def verify_email_token(self, token, request):
        try:
            user, email = verify_email_change_token(token, datetime.timedelta(hours=24))
            if user is None:
                raise NotFound()
            if user.id != request.user.id:
                raise UserNotMached()
            return user, email
        except SignatureExpired:
            raise TokenExpired()
        except BadSignature:
            raise NotFound()

    def get(self, request, token):
        _, email = self.verify_email_token(token, request)
        return Response({"email": email})  # emailも返す?

    def post(self, request, token):
        user, email = self.verify_email_token(token, request)
        user.email = email
        user.save()
        return create_jwt_response(request, user, statuscode=status.HTTP_200_OK)


class ActivationView(GenericAPIView):
    """
    userが他社によって登録されたので、パスワードを設定してactivationする
    """
    serializer_class = api_settings.ACTIVATION_SERIALIZER
    permission_classes = (AllowAny,)
    queryset = get_user_model().objects.none()

    def verify_token(self, token):
        try:
            user = verify_activation_token(token, datetime.timedelta(hours=24))
            if user is None:
                raise NotFound()
            if user.is_active:
                raise UserAlreadyActivated()
            return user
        except SignatureExpired:
            raise TokenExpired()
        except BadSignature:
            raise NotFound()

    def get(self, request, token):
        u = self.verify_token(token)
        return Response({"email": u.email})

    def post(self, request, token):
        user = self.verify_token(token)
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        user.is_active = True
        user.set_password(s.password)
        user.save()
        return create_jwt_response(request, user, statuscode=status.HTTP_200_OK)


class PasswordResetRequestView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EmailSerializer
    queryset = get_user_model().objects.none()

    def post(self, request):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        users = get_user_model().objects.filter(email=s.validated_data['email'])
        for user in users:
            token = create_password_reset_token(user)
            send_passwordreset_email(user, token)
        return Response()


class PasswordResetView(GenericAPIView):
    serializer_class = PasswordSerializer
    permission_classes = (AllowAny,)

    def verify_token(self, token):
        try:
            user = verify_password_reset_token(token, datetime.timedelta(hours=24))
            if user is None:
                raise NotFound()
            return user
        except SignatureExpired:
            raise TokenExpired()
        except BadSignature:
            raise NotFound()

    def get(self, request, token):
        u = self.verify_token(token)
        return Response({"email": u.email})

    def post(self, request, token):
        user = self.verify_token(token)
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        user.is_active = True
        user.set_password(s.password)
        user.save()
        return Response()  # resetの場合は再度loginさせる方が良い気はする


class ResendTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, token):
        try:
            resend_email(token)
        except BadSignature:
            raise NotFound()
        return Response()  # emailを遅れたら空の200を返す


class PasswordChangeView(GenericAPIView):
    serializer_class = PasswordSerializer

    def post(self, request):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        request.user.set_password(s.password)
        request.user.save()
        # 本番では消したほうが良いかもしれない
        update_session_auth_hash(request, request.user)
        return Response()  # 正しくパスワード変更できたら空の200を返す
