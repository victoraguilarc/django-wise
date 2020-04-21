# -*- coding: utf-8 -*-

from json import JSONDecodeError
from django.conf import settings

import requests
import cachecontrol
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.exceptions import NotAuthenticated

from apps.accounts.models import User
from apps.accounts.response_codes import (
    INVALID_GOOGLE_TOKEN_ISSUER,
    INVALID_GOOGLE_TOKEN_ID,
    INVALID_CREDENTIALS,
    INACTIVE_ACCOUNT,
    INVALID_FACEBOOK_ACCESS_TOKEN, INVALID_REFRESH_TOKEN)
from apps.accounts.services.user import UserService


class SessionService(object):
    """Process all related to account sessions."""

    GOOGLE_ACCOUNTS_URL = 'https://accounts.google.com'
    FACEBOOK_USER_URL = 'https://graph.facebook.com/v5.0/me?fields=id,first_name,last_name,email'

    # FACEBOOK_TOKEN_DEBUG_URL = 'https://graph.facebook.com/debug_token'

    @classmethod
    def process_google_token(cls, token: str) -> dict:
        """Returns google account info if is valid.

        https://developers.google.com/identity/sign-in/web/backend-auth
        """
        session = requests.session()
        cached_session = cachecontrol.CacheControl(session)
        request = google_requests.Request(session=cached_session)

        try:
            account_info = id_token.verify_oauth2_token(
                token, request,
                settings.GOOGLE_CLIENT_ID,
            )

            if account_info.get('iss') != cls.GOOGLE_ACCOUNTS_URL:
                raise NotAuthenticated(**INVALID_GOOGLE_TOKEN_ISSUER)

            return UserService.create_or_update_for_social_networks(
                email=account_info.get('email'),
                first_name=account_info.get('first_name'),
                last_name=account_info.get('last_name'),
            )

        except (JSONDecodeError, TypeError, ValueError):
            raise NotAuthenticated(**INVALID_GOOGLE_TOKEN_ID)

    @classmethod
    def make_facebook_profile_url(cls, access_token):
        return '{0}&access_token={1}'.format(cls.FACEBOOK_USER_URL, access_token)

    @classmethod
    def process_facebook_token(cls, access_token: str) -> dict:
        """Returns google account info if is valid."""
        try:
            response = requests.get(cls.make_facebook_profile_url(access_token))
            user_data = response.json()

            if 'error' in user_data:
                raise NotAuthenticated(**INVALID_FACEBOOK_ACCESS_TOKEN)

            return UserService.create_or_update_for_social_networks(
                email=user_data.get('email'),
                first_name=user_data.get('first_name'),
                last_name=user_data.get('last_name'),
            )
        except (ValueError, KeyError, TypeError):
            raise NotAuthenticated(**INVALID_FACEBOOK_ACCESS_TOKEN)

    @classmethod
    def make_user_session(cls, user: User) -> dict:
        """Generates a user JWT session manually."""
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }

    @classmethod
    def validate_session(cls, user, plain_password):
        if user is None or (user and not user.check_password(plain_password)):
            raise NotAuthenticated(**INVALID_CREDENTIALS)

        if not user.is_active:
            raise NotAuthenticated(**INACTIVE_ACCOUNT)

        return True

    @classmethod
    def drop_session(cls, refresh_token):
        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError:
            raise NotAuthenticated(**INVALID_REFRESH_TOKEN)

