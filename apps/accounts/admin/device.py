# -*- coding: utf-8 -*-

from apps.accounts.models import PhoneDevice

from django.contrib import admin


@admin.register(PhoneDevice)
class PhoneDevicedmin(admin.ModelAdmin):
    """Defines the phone device admin behaviour."""

    list_display = (
        'uuid',
        'token',
        'platform',
        'model_name',
        'is_active',
        'user',
    )

    readonly_fields = ['uuid']
