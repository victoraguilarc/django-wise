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

