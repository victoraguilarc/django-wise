
# -*- coding: utf-8 -*-

import pytest

from apps.accounts.models import PendingAction
from apps.accounts.models.choices import ActionCategory
from apps.accounts.services.password_service import PasswordService
from apps.accounts.tests.factories.pending_action import PendingActionFactory


@pytest.mark.django_db
class PasswordServiceTests:

    @staticmethod
    def test_perform_reset_password(test_user):
        pending_action = PasswordService.perform_reset_password(test_user)
        assert isinstance(pending_action, PendingAction)
        assert pending_action.category == ActionCategory.RESET_PASSWORD

    @staticmethod
    def test_confirm_reset_password(test_user):
        plain_password = 'anything'
        pending_action = PendingActionFactory(user=test_user, category=ActionCategory.RESET_PASSWORD)
        PasswordService.confirm_reset_password(pending_action, plain_password)
        updated_pending_action = PendingAction.objects.filter(pk=pending_action.pk).first()

        assert test_user.check_password(plain_password)
        assert updated_pending_action is None

    @staticmethod
    def test_set_pasword(test_user):
        plain_password = 'another_password'
        PasswordService.set_pasword(test_user, plain_password)
        assert test_user.check_password(plain_password)

