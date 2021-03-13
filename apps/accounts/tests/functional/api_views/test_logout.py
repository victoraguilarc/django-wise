# -*- coding: utf-8 -*-

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.api.error_codes import AccountsErrorCodes
from apps.accounts.api.account_responses import AccountsResponses
from apps.contrib.utils.testing.unit_tests import (
    assert_error_code, assert_unauthorized, has_response_format, assert_validation_code,
)


@pytest.mark.django_db
class LogoutTests:

    test_logout_url = reverse('api-accounts:v1:logout')

    def test_invalid_credentials(self, api_client):
        response = api_client.post(self.test_logout_url, {'refreshToken': 'anything'})
        assert_unauthorized(response)

    def test_required_refresh_token(self, auth_api_client):
        response = auth_api_client.post(self.test_logout_url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert_validation_code(
            response_json=response.json(),
            attribute='refreshToken',
            code='required',
        )

    def test_invalid_refresh_token(self, auth_api_client):
        response = auth_api_client.post(self.test_logout_url, {'refreshToken': 'invalid_token'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert_error_code(
            response_json=response.json(),
            code=AccountsErrorCodes.INVALID_REFRESH_TOKEN.code,
        )

    def test_valid_refresh_token(self, api_client, test_user):
        refresh_token = RefreshToken.for_user(test_user)
        access_token = 'Bearer {0}'.format(str(refresh_token.access_token))
        api_client.credentials(HTTP_AUTHORIZATION=access_token)
        response = api_client.post(self.test_logout_url, {'refreshToken': str(refresh_token)})
        response_json = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert has_response_format(response)
        assert response_json.get('code') == AccountsResponses.LOGGED_OUT.get('code')
