# -*- coding: utf-8 -*-

from apps.contrib.email import BaseEmailMessage


class ConfirmEmailMessage(BaseEmailMessage):
    """Email confirmation template."""

    subject = 'transactions/emails/confirm_email/subject.txt'
    message_text = 'transactions/emails/confirm_email/message.txt'
    message_html = 'transactions/emails/confirm_email/message.html'


class ResetPasswordMessage(BaseEmailMessage):
    """Reset password email template."""

    subject = 'transactions/emails/reset_password/subject.txt'
    message_text = 'transactions/emails/reset_password/message.txt'
    message_html = 'transactions/emails/reset_password/message.html'
