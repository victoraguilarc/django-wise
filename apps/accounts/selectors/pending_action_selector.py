from typing import Any

from apps.accounts.models import PendingAction
from apps.accounts.api.error_codes import AccountsErrorCodes


class PendingActionSelector(object):
    """Data layer for PendingAction model."""

    @classmethod
    def get_by_token(cls, token: str, category: str) -> Any:
        """Gets a PendingAction by token."""
        try:
            return PendingAction.objects.get(token=token, category=category)
        except PendingAction.DoesNotExist:
            raise AccountsErrorCodes.INVALID_TOKEN
