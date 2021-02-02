# -*- coding: utf-8 -*-

import pytest
from rest_framework.exceptions import ValidationError

from apps.accounts.models.choices import ActionCategory
from apps.accounts.tests.factories.user import UserFactory
from apps.accounts.services.auth_service import AuthService
from apps.contrib.utils.testing.unit_tests import mail_outbox
from apps.accounts.tests.factories.pending_action import PendingActionFactory


def gen_pending_action(user, email=None):
    extra = {'email': email} if email else {}
    pending_action = PendingActionFactory(
        user=user,
        category=ActionCategory.CONFIRM_EMAIL.value,
        extra=extra,
    )
    return pending_action


@pytest.mark.django_db
class AuthServiceTests:

    @staticmethod
    def test_send_confirmation_email(test_user):
        AuthService.send_confirmation_email(test_user)
        assert mail_outbox() == 1

    @staticmethod
    def test_send_confirmation_email__with_new_email(test_user):
        AuthService.send_confirmation_email(test_user, new_email='new@xiberty.com')
        assert mail_outbox() == 1

    @staticmethod
    def test_confirm_email(test_user):
        test_user.is_active = True
        test_user.save(update_fields=['is_active'])

        pending_action = gen_pending_action(user=test_user)
        AuthService.confirm_email(pending_action)

        test_user.refresh_from_db()
        assert test_user.is_active

    @staticmethod
    def test_confirm_email__new_email(test_user):
        new_email = 'new_email@xiberty.com'
        test_user.is_active = False
        test_user.save(update_fields=['is_active'])

        pending_action = gen_pending_action(test_user, email=new_email)
        AuthService.confirm_email(pending_action)

        assert test_user.is_active
        test_user.refresh_from_db()
        assert test_user.email == new_email

    @staticmethod
    def test_confirm_email__new_email_alredy_used(test_user):
        test_user.email = "existent_email@xiberty.com"
        test_user.save()

        another_user = UserFactory(is_active=False)
        pending_action = gen_pending_action(user=another_user, email=test_user.email)
        with pytest.raises(ValidationError):
            AuthService.confirm_email(pending_action)

        assert another_user.is_active
        assert another_user != test_user.email

    @staticmethod
    def test_confirm_email__invalid_new_email(test_user):
        test_user.is_active = False
        test_user.save()

        pending_action = gen_pending_action(test_user, email='anything')
        with pytest.raises(ValidationError):
            AuthService.confirm_email(pending_action)
        assert test_user.is_active
