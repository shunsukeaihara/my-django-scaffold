from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string

from .settings import api_settings
from .signing import create_email_confirmation_url


def send_confirmation_email(user, token):
    context = {"token_url": create_email_confirmation_url(token)}
    template_prefix = "drf_jwt_util/email/confirmation"
    send_email(user, template_prefix, context)


def send_activation_email(user, token):
    context = {"token_url": create_email_confirmation_url(token)}
    template_prefix = "drf_jwt_util/email/activation"
    send_email(user, template_prefix, context)


def send_passwordreset_email(user, token):
    context = {"token_url": create_email_confirmation_url(token)}
    template_prefix = "drf_jwt_util/email/passwordreset"
    send_email(user, template_prefix, context)


def send_email(user, template_prefix, context):
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
                                     [user.email])
        if 'html' in bodies:
            msg.attach_alternative(bodies['html'], 'text/html')
    else:
        msg = EmailMessage(subject,
                           bodies['html'],
                           from_email,
                           [user.email])
        msg.content_subtype = 'html'
    return msg.send()
