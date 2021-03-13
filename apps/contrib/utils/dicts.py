# -*- coding: utf-8 -*-


def lower_dict_values(dict_obj):
    """It applies lower to all values of a dict."""
    new_dict = {}
    for key, value in dict_obj.items():
        new_dict[key] = value.lower() if isinstance(value, str) else value
    return new_dict
