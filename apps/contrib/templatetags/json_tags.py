# -*- coding: utf-8 -*-

from django import template

from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def form_errors_json(form=None):
    """It prints form errors as JSON."""
    if form:
        return mark_safe(dict(form.errors.items()))  # noqa: S703, S308
    return {}
