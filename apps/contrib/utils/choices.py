# -*- coding: utf-8 -*-


class ListableStrPropsMixin(object):
    @classmethod
    def as_list(cls):
        return [
            value for key, value in cls.__dict__.items()
            if isinstance(value, str) and not key.startswith('__')
        ]
