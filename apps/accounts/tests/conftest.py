# -*- coding: utf-8 -*-

import pytest
import random
from pytest_django.lazy_django import skip_if_no_django

from apps.accounts.models.choices import ActionCategory
from apps.accounts.tests.factories.user import UserFactory

TEST_PASSWORD = 'test_password'


@pytest.fixture
def test_user():
    user = UserFactory()
    user.set_password(TEST_PASSWORD)
    user.save()

    return user


@pytest.fixture
def test_pending_action_category():
    return random.choice([
        ActionCategory.CONFIRM_EMAIL.value,
        ActionCategory.RESET_PASSWORD.value
    ])


@pytest.fixture()
def api_client():
    skip_if_no_django()
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture()
def auth_api_client(db, api_client, test_user):
    from rest_framework_simplejwt.tokens import RefreshToken

    refresh_token = RefreshToken.for_user(test_user)
    access_token = 'Bearer {0}'.format(str(refresh_token.access_token))
    api_client.credentials(HTTP_AUTHORIZATION=access_token)
    return api_client

