from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string

from .settings import api_settings
from .signing import create_email_confirmation_url, create_activation_url, create_password_reset_url
from .signing import get_user_and_tokentype, get_email_from_token
from .signing import TOKEN_EMAIL_CONFIRM, TOKEN_ACTIVATION, TOKEN_PASSWORD_RESET, TOKEN_EMAIL_CHANGE
from. signing import create_email_confirm_token, create_activation_token, create_password_reset_token
from. signing import create_email_change_url, create_email_change_token


def resend_email(old_token):
    user, token_type = get_user_and_tokentype(old_token)
    if token_type == TOKEN_EMAIL_CONFIRM:
        send_confirmation_email(user, create_email_confirm_token(user))
    elif token_type == TOKEN_ACTIVATION:
        send_activation_email(user, create_activation_token(user))
    elif token_type == TOKEN_PASSWORD_RESET:
        send_passwordreset_email(user, create_password_reset_token(user))
    elif token_type == TOKEN_EMAIL_CHANGE:
        email = get_email_from_token(old_token)
        send_email_change_email(email, create_email_change_token(user, email))


def send_confirmation_email(user, token):
    context = {"token_url": create_email_confirmation_url(token)}
    template_prefix = "drf_jwt_util/email/confirmation"
    send_email(user.email, template_prefix, context)


def send_email_change_email(email, token):
    context = {"token_url": create_email_change_url(token)}
    template_prefix = "drf_jwt_util/email/emailchange"
    send_email(email, template_prefix, context)


def send_activation_email(user, token):
    context = {"token_url": create_activation_url(token)}
    template_prefix = "drf_jwt_util/email/activation"
    send_email(user.email, template_prefix, context)


def send_passwordreset_email(user, token):
    context = {"token_url": create_password_reset_url(token)}
    template_prefix = "drf_jwt_util/email/passwordreset"
    send_email(user.email, template_prefix, context)


def send_email(to_email, template_prefix, context):
    from_email = api_settings.FROM_EMAIL
    subject = render_to_string('{0}_subject.txt'.format(template_prefix),
                               context)
    subject = " ".join(subject.splitlines()).strip()

    bodies = {}
    for ext in ['html', 'txt']:
        try:
            template_name = '{0}_message.{1}'.format(template_prefix, ext)
            bodies[ext] = render_to_string(template_name,
                                           context).strip()
        except TemplateDoesNotExist:
            if ext == 'txt' and not bodies:
                raise
    if 'txt' in bodies:
        msg = EmailMultiAlternatives(subject,
                                     bodies['txt'],
                                     from_email,
                                     [to_email])
        if 'html' in bodies:
            msg.attach_alternative(bodies['html'], 'text/html')
    else:
        msg = EmailMessage(subject,
                           bodies['html'],
                           from_email,
                           [to_email])
        msg.content_subtype = 'html'
    return msg.send()
