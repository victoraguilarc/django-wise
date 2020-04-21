# -*- coding: utf-8 -*-

import pytest
from rest_framework.exceptions import NotFound

from apps.accounts.models import User
from apps.accounts.response_codes import USER_NOT_FOUND
from apps.accounts.selectors.user_selector import UserSelector


@pytest.mark.django_db
class UserSelectorTests:

    @staticmethod
    def test_get_by_username(test_user):
        selected_user = UserSelector.get_by_username_or_email(test_user.username)
        assert selected_user is not None
        assert isinstance(selected_user, User)
        assert selected_user == test_user

    @staticmethod
    def test_get_by_email(test_user):
        selected_user = UserSelector.get_by_username_or_email(test_user.email)
        assert selected_user is not None
        assert isinstance(selected_user, User)
        assert selected_user == test_user

    @staticmethod
    def test_get_by_username_or_email_not_found():
        with pytest.raises(NotFound) as exec_info:
            UserSelector.get_by_username_or_email('anything')
        assert exec_info.value.detail.code == USER_NOT_FOUND['code']

