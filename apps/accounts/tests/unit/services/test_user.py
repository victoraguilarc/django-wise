
# -*- coding: utf-8 -*-

import pytest

from apps.accounts.models import User
from apps.contrib.utils.files import generate_image
from apps.accounts.services.user_service import UserService


@pytest.mark.django_db
class UserServiceTests:

    @staticmethod
    def test_update_profile_without_photo(test_user):
        changes = {
            'username': 'cv',
            'first_name': 'corona',
            'last_name': 'virus',
        }
        user = UserService.update_profile(test_user, changes)
        assert isinstance(user, User)
        assert user.username == changes.get('username')
        assert user.first_name == changes.get('first_name')
        assert user.last_name == changes.get('last_name')

    @staticmethod
    def test_update_profile_with_photo(test_user):
        changes = {
            'first_name': 'fulano',
            'last_name': 'de tal',
            'photo': generate_image()
        }
        user = UserService.update_profile(test_user, changes)
        assert isinstance(user, User)
        assert user.first_name == changes.get('first_name')
        assert user.last_name == changes.get('last_name')
        assert user.photo is not None
        assert isinstance(user.photo_url, str)

    @staticmethod
    def test_register_new_user():
        plain_password = 'new_user_password'
        new_user = {
            'email': 'new_user@xiberty.com',
            'password': plain_password,
        }

        is_active = True
        user = UserService.register_new_user(new_user, is_active)
        assert isinstance(user, User)
        assert user.email == new_user.get('email')
        assert user.username == new_user.get('email')
        assert user.is_active == is_active
        assert user.check_password(plain_password)

    @staticmethod
    def test_create_or_update_for_social_networks_if_user_not_exists():
        email = 'facebook_user@xiberty.com'
        first_name = 'fulano'
        last_name = 'de cual'

        user = UserService.create_or_update_for_social_networks(
            email, first_name, last_name,
        )
        assert isinstance(user, User)
        assert user.email == email
        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user.is_active

    @staticmethod
    def test_create_or_update_for_social_networks_if_user_does_not_exists(test_user):
        email = test_user.email
        first_name = 'fulano'
        last_name = 'de cual'

        user = UserService.create_or_update_for_social_networks(
            email, first_name, last_name,
        )
        assert isinstance(user, User)
        assert user == test_user
        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user.is_active


