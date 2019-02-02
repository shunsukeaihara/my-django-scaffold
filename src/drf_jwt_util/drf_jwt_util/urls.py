from django.conf.urls import url
from rest_framework_jwt.views import verify_jwt_token

from .views import refresh_jwt_token, obtain_jwt_token
from .views import ResendTokenView, ActivationView, EmailConfirmView, EmailChangeConfirmView
from .views import PasswordResetView, PasswordResetRequestView


jwturlpatterns = [
    url(r'^login/$', obtain_jwt_token, name="dju_jwt_login"),
    url(r'^verify/$', verify_jwt_token, name="dju_jwt_verify_token"),
    url(r'^refresh/$', refresh_jwt_token, name="dju_jwt_refresh_token")
]

tokenurlpatterns = [
    url(r'^resend/(?P<token>[-:\w]+)/$', ResendTokenView.as_view(), name="dju_resend_token_email"),
    url(r'^activate/(?P<token>[-:\w]+)/$', ActivationView.as_view(), name="dju_activate_token"),
    url(r'^confirm/(?P<token>[-:\w]+)/$', EmailConfirmView.as_view(), name="dju_confirm_token"),
    url(r'^emailconfirm/(?P<token>[-:\w]+)/$', EmailChangeConfirmView.as_view(), name="dju_email_change_confirm_token"),
    url(r'^reset/$', PasswordResetRequestView.as_view(), name="dju_password_reset_request"),
    url(r'^reset/(?P<token>[-:\w]+)/$', PasswordResetView.as_view(), name="dju_password_reset_token"),
]
