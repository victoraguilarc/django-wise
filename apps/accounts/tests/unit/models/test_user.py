# -*- coding: utf-8 -*-
import pytest

from apps.contrib.utils.files import load_test_photo
from apps.accounts.models.user import User
from apps.contrib.utils.testing.decorators import temporarily

from django.utils.translation import ugettext_lazy as _


@pytest.mark.django_db
class UserTests:

    @staticmethod
    def test_string_representation(test_user):
        assert str(test_user) == test_user.email

    @staticmethod
    def test_change_password(test_user):
        new_password = 'new_password'
        test_user.change_password(new_password)
        assert test_user.check_password(new_password)

    @staticmethod
    def test_photo_url_property(test_user):
        assert test_user.photo_url is None
        test_user.photo = load_test_photo()
        test_user.save()
        assert isinstance(test_user.photo_url, str)

    @staticmethod
    def test_full_name_property(test_user):
        full_name = '{0} {1}'.format(test_user.first_name, test_user.last_name)
        assert test_user.full_name == full_name

    @staticmethod
    def test_verbose_name():
        assert str(User._meta.verbose_name) == _('User')

    @staticmethod
    def test_verbose_name_plural():
        assert str(User._meta.verbose_name_plural) == _('Users')

    @staticmethod
    def test_recipient_name(test_user):
        with temporarily(test_user, first_name=''):
            assert test_user.recipient_name == test_user.username
        with temporarily(test_user):
            assert test_user.recipient_name == test_user.first_name

    @staticmethod
    def test_save_without_username(test_user):
        test_user.username = ' '
        test_user.save()
        assert test_user.username == test_user.email

        test_user.username = None
        test_user.save()
        assert test_user.username == test_user.email

