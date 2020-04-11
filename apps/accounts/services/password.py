# -*- coding: utf-8 -*-

from apps.accounts.models import User, PendingAction
from apps.accounts.models.choices import ActionCategory
from apps.contrib.utils.strings import get_lapse


class PasswordService(object):
    """Process all related to account sessions."""

    @classmethod
    def perform_reset_password(cls, user: User) -> PendingAction:
        pending_action, created = PendingAction.objects.get_or_create(
            user=user,
            category=ActionCategory.RESET_PASSWORD,
        )

        creation_date, expiration_date = get_lapse()
        pending_action.creation_date = creation_date
        pending_action.expiration_date = expiration_date
        pending_action.save(update_fields=['creation_date', 'expiration_date'])

        return pending_action

    @classmethod
    def confirm_reset_password(cls, pending_action: PendingAction, plain_password: str):
        pending_action.user.set_password(plain_password)
        pending_action.delete()

    @classmethod
    def set_pasword(cls, user: User, plain_password: str) -> None:
        user.set_password(plain_password)
        user.save()

