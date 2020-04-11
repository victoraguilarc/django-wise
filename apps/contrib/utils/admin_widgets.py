# -*- coding: utf-8 -*-

from django.contrib.admin.widgets import FilteredSelectMultiple

from django.utils.datastructures import MultiValueDict


class ArrayFieldSelectMultiple(FilteredSelectMultiple):
    """Overrides the regular widget for arrays by the another pretty awesome."""

    def __init__(self, verbose_name, is_stacked=False, *args, **kwargs):  # noqa: D107
        self.delimiter = kwargs.pop('delimiter', ',')
        super().__init__(verbose_name, is_stacked, *args, **kwargs)

    def render(self, name, field_value, attrs=None, renderer=None):  # noqa: D102
        if isinstance(field_value, str):
            field_value = field_value.split(self.delimiter)
        return super().render(name, field_value, attrs, renderer)

    def value_from_datadict(self, options_data, files, name):  # noqa: D107, D102
        if isinstance(options_data, MultiValueDict):
            # Normally, we'd want a list here, which is what we get from the
            # SelectMultiple superclass, but the SimpleArrayField expects to
            # get a delimited string, so we're doing a little extra work.
            return self.delimiter.join(options_data.getlist(name))
        return options_data.get(name, None)
