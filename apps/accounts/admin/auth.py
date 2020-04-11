# -*- coding: utf-8 -*-

from django.contrib import admin
from apps.accounts.models.pending_action import PendingAction


@admin.register(PendingAction)
class PendingActiondmin(admin.ModelAdmin):
    """Defines the pending action admin behaviour."""

    list_display = (
        'token',
        'user',
        'category',
        'creation_date',
        'expiration_date',
    )
