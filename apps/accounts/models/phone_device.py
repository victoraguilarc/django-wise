# -*- coding: utf-8 -*-

from django.db import models

from apps.contrib.models.mixins import TimeStampedModelMixin, UUIDPrimaryKeyModelMixin
from apps.accounts.models.choices import Platform
from apps.accounts.models.managers.phone_device import PhoneDeviceManager

from django.utils.translation import ugettext_lazy as _


class PhoneDevice(UUIDPrimaryKeyModelMixin, TimeStampedModelMixin):
    """Represents the user phone device."""

    token = models.TextField(
        verbose_name=_('Device ID'),
        db_index=True,
        blank=True,
        null=True,
    )

    platform = models.CharField(
        choices=Platform.choices(),
        max_length=10,
    )

    model_name = models.CharField(
        max_length=50,
        verbose_name=_('Model Name'),
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        verbose_name=_('Is active'),
        default=True,
    )

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='devices',
        blank=True,
        null=True,
    )

    objects = PhoneDeviceManager()

    def __str__(self):
        return '{token} - {user}'.format(
            token=self.token,
            user=self.user,
        )

    class Meta:
        db_table = 'phone_devices'
        verbose_name = _('Phone Device')
        verbose_name_plural = _('Phone Devices')
        ordering = ['created_at']
        app_label = 'accounts'
