# -*- coding: utf-8 -*-

from apps.contrib.api.exceptions.base import (
    APINotFound, APIBadRequest, APINotAuthenticated, APIPermissionDenied, APIAuthenticationFailed,
)

from django.utils.translation import ugettext_lazy as _


class AccountsErrorCodes(object):
    """These are all common account error codes."""

    # >> Authentication

    INVALID_GOOGLE_TOKEN_ID = APIAuthenticationFailed(
        code='auth.InvalidGoogleTokenID',
        detail=_('The token is corrupted or expired'),
    )

    INVALID_GOOGLE_TOKEN_ISSUER = APIAuthenticationFailed(
        code='auth.InvalidGoogleTokenIssuer',
        detail=_('The token was issued for an invalid provider'),
    )

    INVALID_FACEBOOK_ACCESS_TOKEN = APIAuthenticationFailed(
        code='auth.InvalidFacebookAccessToken',
        detail=_('The access token is corrupted or expired'),
    )

    INVALID_REFRESH_TOKEN = APIAuthenticationFailed(
        code='auth.InvalidRefreshToken',
        detail=_('Invalid Refresh token'),
    )

    UNAUTHORIZED_ACCOUNT = APINotAuthenticated(
        code='auth.UnauthorizedAccount',
        detail=_('This account is unauthorized'),
    )

    CREDENTIALS_REQUIRED = APIAuthenticationFailed(
        code='credentials_required',
        detail=_('Email/username and password are required'),
    )

    INACTIVE_ACCOUNT = APIAuthenticationFailed(
        code='auth.InactiveAccount',
        detail=_('The account is not active'),
    )

    UNVERIFIED_EMAIL = APIAuthenticationFailed(
        code='auth.UnverifiedEmail',
        detail=_('Email must be verified'),
    )

    INVALID_CREDENTIALS = APINotAuthenticated(
        code='auth.InvalidCredentials',
        detail=_('User/email and password credentials are invalid'),
    )

    INVALID_TOKEN = APINotAuthenticated(
        code='auth.InvalidToken',
        detail=_('This token is invalid or expired'),
    )

    USER_NOT_FOUND = APINotFound(
        code='accounts.UserNotFound',
        detail=_('User not Found'),
    )

    EMAIL_ALREDY_USED = APIBadRequest(
        code='auth.EmailIsAlreadyUsed',
        detail=_('This email is already being used.'),
    )

    USERNAME_ALREDY_USED = APIBadRequest(
        code='auth.UsernameIsAlreadyUsed',
        detail=_('The username is already being used.'),
    )

    AUTHENTICATION_FAILED = APINotAuthenticated(
        code='auth.AuthenticationFailed',
        detail=_('The authentication process failed, try again.'),
    )

    PERMISSION_DENIED = APIPermissionDenied(
        code='auth.PermissionDenied',
        detail=_('You do not have permission to perform this action.'),
    )

    # >> Users

    USERNAME_UNAVAILABLE = APIBadRequest(
        code='accounts.UsernameUnavailable',
        detail=_('This username is being used by another user'),
    )

    INVALID_PASSWORD = APIBadRequest(
        code='accounts.InvalidPassword',
        detail=_('Invalid password. Try again.'),
    )

    PASSWORD_MISTMATCH = APIBadRequest(
        code='accounts.PasswordMistmatch',
        detail=_('The Passwords mistmatch'),
    )

    USER_HAS_PASSWORD = APIBadRequest(
        code='accounts>UserHasPassword',
        detail=_('You can only set password for users who do not have it, this user already has one'),
    )

    DEVICE_NOT_FOUND = APINotFound(
        code='accounts.DeviceNotFound',
        detail=_('Device Not found'),
    )
