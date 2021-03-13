# -*- coding: utf-8 -*-

import pytest
from faker import Factory
from django.urls import reverse
from rest_framework import status
from faker.providers import misc, lorem

from apps.contrib.utils.files import generate_image
from apps.accounts.api.error_codes import AccountsErrorCodes
from apps.accounts.tests.factories.user import UserFactory, generate_user_profile
from apps.contrib.utils.testing.unit_tests import assert_validation_code

faker = Factory.create()
faker.add_provider(misc)
faker.add_provider(lorem)


@pytest.mark.django_db
class ProfileViewSetTests:

    profile_url = reverse('api-accounts:v1:profile')

    def test_get_profile(self, auth_api_client, test_user):
        response = auth_api_client.get(self.profile_url)
        user_profile = response.json()
        required_keys = {'username', 'firstName', 'lastName', 'email', 'photo'}
        assert user_profile.keys() & required_keys
        assert response.status_code == status.HTTP_200_OK

    def test_get_profile_credentials_required(self, api_client):
        response = api_client.get(self.profile_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @classmethod
    def assert_profile(cls, response, new_profile):
        user_profile = response.json()
        required_keys = {'username', 'firstName', 'lastName', 'email', 'photo'}
        has_required_keys = user_profile.keys() & required_keys

        assert has_required_keys
        assert new_profile['username'] == user_profile['username']
        assert new_profile['firstName'] == user_profile['firstName']
        assert new_profile['lastName'] == user_profile['lastName']

    def test_update_profile(self, auth_api_client):
        profile = generate_user_profile()
        response = auth_api_client.put(self.profile_url, data=profile)
        assert response.status_code == status.HTTP_200_OK
        self.assert_profile(response, profile)

    def test_update_profile_crendentials_required(self, api_client):
        profile = generate_user_profile()
        response = api_client.put(self.profile_url, data=profile)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_profile__with_photo(self, auth_api_client):
        profile = generate_user_profile()
        profile['photo'] = generate_image()

        response = auth_api_client.put(
            self.profile_url,
            data=profile,
            format='multipart',
        )
        assert response.status_code == status.HTTP_200_OK
        self.assert_profile(response, profile)

    def test_update_profile_alredy_used_username(self, auth_api_client):
        existent_user = UserFactory()
        profile = generate_user_profile()
        profile['username'] = existent_user.username

        response = auth_api_client.put(self.profile_url, data=profile)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert_validation_code(
            response_json=response.json(),
            attribute='username',
            code=AccountsErrorCodes.USERNAME_UNAVAILABLE.code,
        )
