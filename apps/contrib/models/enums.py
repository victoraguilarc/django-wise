# -*- coding: utf-8 -*-

from enum import Enum


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
