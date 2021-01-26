import pytest

from apps.accounts.forms import UserCreationForm
from apps.accounts.admin.user import UserCreationForm as UserCreationAdminForm
from apps.accounts.models.user import User
from apps.accounts.tests.factories.user import generate_user_profile

from django.utils.translation import ugettext_lazy as _


def get_profile():
    data = generate_user_profile()
    password = data.pop('password')
    data['password1'] = password
    data['password2'] = password
    return data


@pytest.mark.django_db
class UserCreationFormTests:

    @staticmethod
    def test_valid_data():
        form = UserCreationForm(data=get_profile())
        assert form.is_valid()
        user = form.save()
        assert isinstance(user, User)

    @staticmethod
    def test_invalid_data():
        data = get_profile()
        del data['username']
        form = UserCreationForm(data=data)
        assert not form.is_valid()

    @staticmethod
    def test_blank_data():
        form = UserCreationForm(data={})
        assert not form.is_valid()

    @staticmethod
    def test_clean_passwords():
        data = get_profile()
        data['password2'] = 'anything'
        form = UserCreationForm(data=data)
        assert not form.is_valid()
        assert form.errors == {'password2': [_('Passwords Mismatch')]}


@pytest.mark.django_db
class UserCreationAdminFormTests:

    @staticmethod
    def test_clean_invalid_username(test_user):
        test_user.refresh_from_db()
        data = get_profile()
        data['username'] = test_user.username
        form = UserCreationAdminForm(data=data)
        assert not form.is_valid()

    @staticmethod
    def test_clean_valid_username():
        data = get_profile()
        form = UserCreationAdminForm(data=data)
        assert form.is_valid()
