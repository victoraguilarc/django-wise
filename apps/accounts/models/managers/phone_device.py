# -*- coding: utf-8 -*-

from django.db import models


class PhoneDeviceManager(models.Manager):
    """Contains extra phone devices queries."""

    def get_queryset(self):
        return PhoneDeviceQuerySet(self.model)


class PhoneDeviceQuerySet(models.query.QuerySet):
    """It will be contains the most common queries for phone devices."""
