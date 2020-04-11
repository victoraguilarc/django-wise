# -*- coding: utf-8 -*-

from django.apps import AppConfig


class ContribConfig(AppConfig):
    """Configuration for project utilities."""

    name = 'apps.contrib'
    verbose_name = 'Contrib'

    def ready(self):
        """Override this to put in.

        Users system checks
        Users signal registration
        """
