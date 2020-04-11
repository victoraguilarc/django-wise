# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def send_email(subject, to, text_body, html_body):
    """Helps to send and email."""
    email = EmailMultiAlternatives(
        subject=subject,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to, body=text_body,
    )

    email.attach_alternative(html_body, 'text/html')
    email.send()
