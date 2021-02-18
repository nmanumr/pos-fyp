from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string

from xmodule.tasks import send_mail


def send_template_mail(context, directory, recipients, sender_email=None, fail_silently=True):
    subject = render_to_string(directory + '/subject.txt', context)
    context['subject'] = subject
    plain_body = render_to_string(directory + '/body.txt', context)

    try:
        html_body = render_to_string(directory + '/body.html', context)
    except TemplateDoesNotExist:
        html_body = None

    send_mail.delay(
        subject=subject,
        recipients=recipients,
        body_html=html_body,
        body_text=plain_body,
        sender=sender_email,
        fail_silently=fail_silently
    )
