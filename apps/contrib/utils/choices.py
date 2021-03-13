# -*- coding: utf-8 -*-


class ListableStrPropsMixin(object):
    """Mixing to sintetize Enum common methods."""

    @classmethod
    def as_list(cls):
        """Returns properties as a list."""
        return [
            value for key, value in cls.__dict__.items()
            if isinstance(value, str) and not key.startswith('__')
        ]
