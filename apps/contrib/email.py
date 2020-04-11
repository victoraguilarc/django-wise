# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class BaseEmailMessage:
    """Provides the basic functionalty to email template classes."""

    subject = None
    message_html = None
    message_text = None

    def __init__(self, context=None):  # noqa: D107
        self.context = context or {}

    def _get_args(self):
        """Makes the email arguments."""
        subject = render_to_string(template_name=self.subject, context=self.context)
        text_body = render_to_string(template_name=self.message_text, context=self.context)
        html_body = render_to_string(template_name=self.message_html, context=self.context)
        return subject, text_body, html_body

    def send(self, to, subject=None, from_email=None):
        """Sends email with the some arguments."""
        from_email = from_email or settings.DEFAULT_FROM_EMAIL
        to_emais = [to] if not isinstance(to, list) else to

        argument_subject, text_body, html_body = self._get_args()
        subject = subject or argument_subject

        email = EmailMultiAlternatives(
            subject=subject,
            from_email=from_email,
            to=to_emais,
            body=text_body,
        )
        email.attach_alternative(html_body, 'text/html')
        email.send()
