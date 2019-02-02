# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework_jwt.compat import PasswordField
from rest_framework_jwt.serializers import RefreshJSONWebTokenSerializer as OrigRefreshJSONWebTokenSerializer
from rest_framework_jwt.serializers import JSONWebTokenSerializer

UserModel = get_user_model()


def get_username_field():
    try:
        username_field = UserModel.USERNAME_FIELD
    except AttributeError:
        username_field = 'username'

    return username_field


def get_field_by_name(option, name):
    fields = {f.name: f for f in option.fields}
    if name not in fields:
        return serializers.CharField()()
    field = fields[name]
    if field.__class__ not in serializers.ModelSerializer.serializer_field_mapping:
        return serializers.CharField()
    return serializers.ModelSerializer.serializer_field_mapping[field.__class__]()


class ObtainJSONWebTokenSerializer(JSONWebTokenSerializer):
    def __init__(self, *args, **kwargs):
        super(JSONWebTokenSerializer, self).__init__(*args, **kwargs)
        self.fields[get_username_field()] = get_field_by_name(UserModel._meta, get_username_field())
        self.fields['password'] = PasswordField(write_only=True)


class RefreshJSONWebTokenSerializer(OrigRefreshJSONWebTokenSerializer):
    def _check_user(self, payload):
        uid = payload['uid']
        if not uid:
            msg = _('Invalid payload.')
            raise serializers.ValidationError(msg)
        try:
            user = get_user_model().objects.get(id=uid)
        except UserModel.DoesNotExist:
            msg = _("User doesn't exist.")
            raise serializers.ValidationError(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise serializers.ValidationError(msg)

        return user


class DefaultUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["pk", "email", "username"]
        read_only_fields = [get_username_field()]


class ValidatePasswordMixin:
    def validate_password1(self, value):
        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password2": _("You must type the same email each time.")})
        self.password = data["password1"]
        return data


class RegisterSerializer(ValidatePasswordMixin, serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [get_username_field(), "password1", "password2"]
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def save(self, **kwargs):
        user = super(RegisterSerializer, self).save(**kwargs)
        user.set_password(self.password)
        user.save()
        return user


class PasswordSerializer(ValidatePasswordMixin, serializers.Serializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
