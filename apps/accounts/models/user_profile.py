# -*- coding: utf-8 -*-

from django.db import models

from apps.contrib.models.mixins import TimeStampedModelMixin

from django.utils.translation import ugettext_lazy as _


class UserProfile(TimeStampedModelMixin):
    """This class is to customize some extra fields for users. e.g. roles."""

    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='user_profile',
    )

    def __str__(self):
        return self.user.email

    class Meta:
        db_table = 'user_profiles'
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
        app_label = 'accounts'
