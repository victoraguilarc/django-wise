# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _


class AccountsResponses(object):
    """These are all common accoun responses."""

    #
    #  A U T H E N T I C A T I O N
    #

    RESET_PASSWORD_SENT = {
        'code': 'accounts.ResetPasswordSent',
        'message': _('An email to restore password was sent'),
    }

    CONFIRMATION_EMAIL_SENT = {
        'code': 'accounts.EmailConfirmationSent',
        'message': _('Email confirmation sent'),
    }

    EMAIL_VERIFIED = {
        'code': 'accounts.VerifiedEmail',
        'message': _('Your email has already been verified'),
    }

    #
    #  U S E R S
    #

    PASSWORD_UPDATED = {
        'code': 'accounts.PasswordUpdated',
        'message': _('Password updated successfully'),
    }

    PASSWORD_ADDED = {
        'code': 'accounts.PasswordConfigured',
        'message': _('Password has configured successfully'),
    }

    LOGGED_OUT = {
        'code': 'accounts.SucessfulLogout',
        'message': _('You have successfully logged out.'),
    }

    DEVICE_REGISTERED = {
        'code': 'accounts.RegisteredDevice',
        'message': _('Registered Device.'),
    }
