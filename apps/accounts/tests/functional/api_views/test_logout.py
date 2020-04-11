# -*- coding: utf-8 -*-

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.response_codes import INVALID_REFRESH_TOKEN, LOGGED_OUT
from apps.contrib.utils.tests.unit_tests import has_unauthorized, has_response_format


@pytest.mark.django_db
class LogoutTests:

    test_logout_url = reverse('api-accounts:v1:logout')

    def test_invalid_credentials(self, api_client):
        response = api_client.post(self.test_logout_url, {'refresh_token': 'anything'})
        assert has_unauthorized(response)

    def test_required_refresh_token(self, auth_api_client):
        response = auth_api_client.post(self.test_logout_url, {})
        response_json =  response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'refresh_token' in response_json
        assert response_json['refresh_token'][0]['code'] == 'required'

    def test_invalid_refresh_token(self, auth_api_client):
        response = auth_api_client.post(self.test_logout_url, {'refresh_token': 'invalid_token'})
        response_json = response.json()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert has_response_format(response)
        assert response_json.get('code') == INVALID_REFRESH_TOKEN.get('code')
    #
    def test_valid_refresh_token(self, api_client, test_user):
        refresh_token = RefreshToken.for_user(test_user)
        access_token = 'Bearer {0}'.format(str(refresh_token.access_token))
        api_client.credentials(HTTP_AUTHORIZATION=access_token)
        response = api_client.post(self.test_logout_url, {'refresh_token': str(refresh_token)})
        response_json = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert has_response_format(response)
        assert response_json.get('code') == LOGGED_OUT.get('code')
