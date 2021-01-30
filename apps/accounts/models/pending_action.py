# -*- coding: utf-8 -*-

import uuid
from django.db import models
from django.db.models import JSONField
from django.core.serializers.json import DjangoJSONEncoder

from apps.contrib.models.mixins import UUIDWithTimestampMixin
from apps.accounts.models.choices import ActionCategory

from django.utils.translation import ugettext_lazy as _


class PendingAction(UUIDWithTimestampMixin):
    """Represents an user actions that it must be completed."""

    user = models.ForeignKey(
        'accounts.User',
        verbose_name=_('User'),
        related_name='pending_actions',
        on_delete=models.CASCADE,
    )

    category = models.CharField(
        max_length=50,
        choices=ActionCategory.choices(),
        db_index=True,
    )

    token = models.CharField(
        max_length=150,
        db_index=True,
        default=uuid.uuid4,
    )

    creation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(blank=True, null=True)

    extra = JSONField(
        encoder=DjangoJSONEncoder,
        verbose_name=_('extra'),
        help_text=_('This field changes according to the type of action'),
        default=dict,
        blank=True,
    )

    def __str__(self):
        return self.token

    class Meta:
        db_table = 'pending_actions'
        verbose_name = _('Pending Action')
        verbose_name_plural = _('Pending Actions')
        app_label = 'accounts'
