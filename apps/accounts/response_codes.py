# -*- coding: utf-8 -*-

from rest_framework import status
from django.utils.translation import ugettext_lazy as _

# ~ ERRORS
# --------------------------------------------

# >> Authentication

INVALID_GOOGLE_TOKEN_ID = {
    'code': 'auth.InvalidGoogleTokenID',
    'detail': _('The token is corrupted or expired'),
}

INVALID_GOOGLE_TOKEN_ISSUER = {
    'code': 'auth.InvalidGoogleTokenIssuer',
    'detail': _('The token was issued for an invalid provider'),
}

INVALID_FACEBOOK_ACCESS_TOKEN = {
    'code': 'auth.InvalidFacebookAccessToken',
    'detail': _('The access token is corrupted or expired'),
}

INVALID_REFRESH_TOKEN = {
    'code': 'auth.InvalidRefreshToken',
    'detail': _('Invalid Refresh token'),
}

UNAUTHORIZED_ACCOUNT = {
    'code': 'auth.UnauthorizedAccount',
    'detail': _('This account is unauthorized'),
}

VALID_OPERATOR_ACCOUNT_REQUIRED = {
    'code': 'auth.ValidOperatorAccountRequired',
    'detail': _('A valid operator account is required'),
}

CREDENTIALS_REQUIRED = {
    'code': 'credentials_required',
    'detail': _('Email/username and password are required'),
}

INACTIVE_ACCOUNT = {
    'code': 'auth.InactiveAccount',
    'detail': _('The account is not active'),
}

UNVERIFIED_EMAIL = {
    'code': 'auth.UnverifiedEmail',
    'detail': _('Email must be verified'),
}

INVALID_CREDENTIALS = {
    'code': 'auth.InvalidCredentials',
    'detail': _('User/email and password credentials are invalid'),
}

INVALID_TOKEN = {
    'code': 'auth.InvalidToken',
    'detail': _('This token is invalid or expired'),
}

USER_NOT_FOUND = {
    'code': 'accounts.UserNotFound',
    'detail': _('User not Found'),
}

EMAIL_ALREDY_USED = {
    'code': 'auth.EmailIsAlreadyUsed',
    'detail': _('This email is already being used.'),
}

USERNAME_ALREDY_USED = {
    'code': 'auth.UsernameIsAlreadyUsed',
    'detail': _('The username is already being used.'),
}

AUTHENTICATION_FAILED = {
    'code': 'auth.AuthenticationFailed',
    'detail': _('The authentication process failed, try again.'),
}

PERMISSION_DENIED = {
    'code': 'auth.PermissionDenied',
    'message': _('You do not have permission to perform this action.'),
}

# >> Users

USERNAME_UNAVAILABLE = {
    'code': 'accounts.UsernameUnavailable',
    'detail': _('This username is being used by another user'),
}

INVALID_PASSWORD = {
    'code': 'accounts.InvalidPassword',
    'detail': _('Invalid password. Try again.'),
}

PASSWORD_MISTMATCH = {
    'code': 'accounts.PasswordMistmatch',
    'detail': _('The Passwords mistmatch'),
}

USER_HAS_PASSWORD = {
    'code': 'user_has_valid_password',
    'detail': _('You can only set password for users who do not have it, this user already has one'),
}

DEVICE_NOT_FOUND = {
    'code': 'accounts.DeviceNotFound',
    'detail': _('Device Not found'),
}

# ~ SUCCESS
# --------------------------------------------

# >> Authentication

RESET_PASSWORD_SENT = {
    'code': 'accounts.ResetPasswordSent',
    'detail': _('An email to restore password was sent'),
}

CONFIRMATION_EMAIL_SENT = {
    'code': 'accounts.EmailConfirmationSent',
    'detail': _('Email confirmation sent'),
}


EMAIL_VERIFIED = {
    'code': 'accounts.VerifiedEmail',
    'detail': _('Your email has already been verified'),
}

# >> Users

PASSWORD_UPDATED = {
    'code': 'accounts.PasswordUpdated',
    'detail': _('Password updated successfully'),
}

PASSWORD_ADDED = {
    'code': 'accounts.PasswordConfigured',
    'detail': _('Password has configured successfully'),
    'status': status.HTTP_201_CREATED,
}

LOGGED_OUT = {
    'code': 'accounts.SucessfulLogout',
    'detail': _('You have successfully logged out.'),
}

DEVICE_REGISTERED = {
    'code': 'accounts.RegisteredDevice',
    'detail': _('Registered Device.'),
}
