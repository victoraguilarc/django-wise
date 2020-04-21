# -*- coding: utf-8 -*-
import pytest

from apps.accounts.models.choices import ActionCategory
from apps.accounts.services.auth_email import AuthEmailService
from apps.accounts.tests.factories.pending_action import PendingActionFactory
from apps.contrib.utils.tests.unit_tests import mail_outbox


@pytest.mark.django_db
class EmailServiceTests:

    @staticmethod
    def test_send_confirm_email(test_user):
        AuthEmailService.send_confirm_email(
            PendingActionFactory(user=test_user, category=ActionCategory.CONFIRM_EMAIL)
        )
        assert mail_outbox() == 1

    @staticmethod
    def test_send_reset_password(test_user):
        AuthEmailService.send_reset_password(
            PendingActionFactory(user=test_user, category=ActionCategory.RESET_PASSWORD)
        )
        assert mail_outbox() == 1
