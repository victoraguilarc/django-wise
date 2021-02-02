from typing import Any

from apps.accounts.api.error_codes import AccountsErrorCodes
from apps.accounts.models import PendingAction


class PendingActionSelector(object):

    @classmethod
    def get_by_token(cls, token: str, category: str) -> Any:
        try:
            return PendingAction.objects.get(token=token, category=category)
        except PendingAction.DoesNotExist:
            raise AccountsErrorCodes.INVALID_TOKEN
