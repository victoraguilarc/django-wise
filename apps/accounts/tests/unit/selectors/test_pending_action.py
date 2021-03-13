# -*- coding: utf-8 -*-

import pytest

from apps.accounts.api.error_codes import AccountsErrorCodes
from apps.contrib.api.exceptions.base import APIBaseException
from apps.accounts.tests.factories.pending_action import PendingActionFactory
from apps.accounts.selectors.pending_action_selector import PendingActionSelector


@pytest.mark.django_db
class PendingActionSelectorTests:

    @staticmethod
    def test_get_by_token(test_pending_action_category):
        pending_action = PendingActionFactory(category=test_pending_action_category)
        selected_pending_action = PendingActionSelector.get_by_token(
            pending_action.token,
            test_pending_action_category,
        )
        assert selected_pending_action is not None
        assert selected_pending_action == pending_action

    @staticmethod
    def test_get_by_token_not_found(test_pending_action_category):
        with pytest.raises(APIBaseException) as exec_info:
            PendingActionSelector.get_by_token(
                'anything',
                test_pending_action_category,
            )
        assert exec_info.value.detail.code == AccountsErrorCodes.INVALID_TOKEN.code

