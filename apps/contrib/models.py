# -*- coding: utf-8 -*-

import uuid
from enum import Enum
from django.db import models


class BaseEnum(Enum):
    """Provides the common functionalties to multiple model choices."""

    @classmethod
    def choices(cls):
        return [(option.value, option.value) for option in cls]

    @classmethod
    def values(cls):
        return [option.value for option in cls]

    def __str__(self):
        return str(self.value)


class TimeStampedModelMixin(models.Model):
    """Timestamp extra field.

    An abstract base class model that provides self updating 'created' and 'modified' fields
    https://docs.djangoproject.com/en/2.1/ref/models/fields/#django.db.models.DateField.auto_now_add
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class UUIDModelMixin(models.Model):
    """An abstract base class model that provides an uuid field."""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class SlugModelMixin(models.Model):
    """An abstract base class model that provides a slug field."""

    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        abstract = True


class UUIDPrimaryKeyModelMixin(models.Model):
    """An abstract base class model that provides an uuid field that is the primary key."""

    uuid = models.UUIDField(
        verbose_name='UUID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True
