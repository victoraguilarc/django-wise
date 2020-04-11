import pytest

from apps.accounts.tests.factories.user import UserFactory


@pytest.fixture
def test_user():
    return UserFactory()

