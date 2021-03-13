
# -*- coding: utf-8 -*-

import json
import pytest
import requests_mock
from doubles import allow
from google.oauth2 import id_token
from rest_framework import status

from apps.accounts.models import User
from apps.accounts.api.error_codes import AccountsErrorCodes
from apps.contrib.api.exceptions.base import APIBaseException
from apps.accounts.services.user_service import UserService
from apps.accounts.services.session_service import SessionService


@pytest.mark.django_db
class SessionServiceTests:

    @staticmethod
    def test_process_google_token(test_user):
        allow(id_token).verify_oauth2_token.and_return({
           'iss': SessionService.GOOGLE_ACCOUNTS_URL,
        })
        allow(UserService).create_or_update_for_social_networks.and_return(test_user)

        user = SessionService.process_google_token('valid_token')
        assert user is not None
        assert isinstance(user, User)

    @staticmethod
    def test_process_google_token_invalid_issuer():
        allow(id_token).verify_oauth2_token.and_return({
            'iss': 'https://any.server',
        })
        with pytest.raises(APIBaseException) as exec_info:
            SessionService.process_google_token('valid_token')
        assert exec_info.value.detail.code == AccountsErrorCodes.INVALID_GOOGLE_TOKEN_ISSUER.code

    @staticmethod
    def test_process_google_token_invalid_token():
        allow(id_token).verify_oauth2_token.and_raise(ValueError('Token Error'))

        with pytest.raises(APIBaseException) as exec_info:
            SessionService.process_google_token('valid_token')
        assert exec_info.value.detail.code == AccountsErrorCodes.INVALID_GOOGLE_TOKEN_ID.code

    @staticmethod
    def test_process_facebook_valid_access_token(test_user):
        allow(UserService).create_or_update_for_social_networks.and_return(test_user)
        access_token = 'valid_access_token'
        with requests_mock.mock() as mock:
            mock.get(
                SessionService.make_facebook_profile_url(access_token),
                text=json.dumps({
                    'email': test_user.email,
                    'first_name': test_user.first_name,
                    'last_name': test_user.last_name,
                }),
                status_code=status.HTTP_200_OK,
            )

            user = SessionService.process_facebook_token(access_token)

        assert user is not None
        assert isinstance(user, User)

    @staticmethod
    def test_process_facebook_token_invalid_access_token():
        access_token = 'invalid_access_token'
        with requests_mock.mock() as mock:
            mock.get(
                SessionService.make_facebook_profile_url(access_token),
                text=json.dumps({'error': 'facebook_raised_error'}),
                status_code=status.HTTP_200_OK,
            )
            with pytest.raises(APIBaseException) as exec_info:
                SessionService.process_facebook_token(access_token)
            assert exec_info.value.detail.code == AccountsErrorCodes.INVALID_FACEBOOK_ACCESS_TOKEN.code

    @staticmethod
    def test_process_facebook_token_invalid_access_token_from_format(test_user):
        access_token = 'invalid_access_token'
        with requests_mock.mock() as mock:
            mock.get(
                SessionService.make_facebook_profile_url(access_token),
                text='',
                status_code=status.HTTP_200_OK,
            )
            with pytest.raises(APIBaseException) as exec_info:
                SessionService.process_facebook_token(access_token)
            assert exec_info.value.detail.code == AccountsErrorCodes.INVALID_FACEBOOK_ACCESS_TOKEN.code

    @staticmethod
    def test_make_user_session(test_user):
        session = SessionService.make_user_session(test_user)
        assert 'access_token' in session
        assert 'refresh_token' in session

    @staticmethod
    def test_validate_session(test_user):
        plain_password = 'new_password'
        test_user.set_password(plain_password)
        test_user.save()

        assert SessionService.validate_session(test_user, plain_password)

    @staticmethod
    def test_validate_session_invalid_credentials(test_user):
        with pytest.raises(APIBaseException) as exec_info:
            SessionService.validate_session(None, 'new_password')
        assert exec_info.value.detail.code == AccountsErrorCodes.INVALID_CREDENTIALS.code

        with pytest.raises(APIBaseException) as exec_info:
            SessionService.validate_session(test_user, 'new_password')
        assert exec_info.value.detail.code == AccountsErrorCodes.INVALID_CREDENTIALS.code

    @staticmethod
    def test_validate_session_inactive_account(test_user):
        plain_password = 'another_password'
        test_user.set_password(plain_password)
        test_user.is_active = False
        test_user.save()

        with pytest.raises(APIBaseException) as exec_info:
            SessionService.validate_session(test_user, plain_password)
        assert exec_info.value.detail.code == AccountsErrorCodes.INACTIVE_ACCOUNT.code
