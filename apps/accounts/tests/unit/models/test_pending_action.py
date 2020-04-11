# -*- coding: utf-8 -*-
import pytest

from apps.accounts.models.pending_action import PendingAction
from apps.accounts.tests.factories.pending_action import PendingActionFactory

from django.utils.translation import ugettext_lazy as _


@pytest.mark.django_db
class PendingActionModelTests:

    @staticmethod
    def test_string_representation():
        pending_action = PendingActionFactory()
        assert str(pending_action) == pending_action.token

    @staticmethod
    def test_verbose_name():
        assert str(PendingAction._meta.verbose_name) == _('Pending Action')

    @staticmethod
    def test_verbose_name_plural():
        assert str(PendingAction._meta.verbose_name_plural) == _('Pending Actions')
