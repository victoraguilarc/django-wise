# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from apps.accounts.models import User


class Command(BaseCommand):
    """Creates a superuser."""

    help = 'Touch a superuser!'  # noqa: WPS125

    def handle(self, *args, **options):
        """Creates a superuser admin."""
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@admin.com', 'D1451E44D717AF8E')
