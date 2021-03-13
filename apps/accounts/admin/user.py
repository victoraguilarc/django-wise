# -*- coding: utf-8 -*-

from django import forms

from apps.accounts.models.user import User

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm as UserChangeFormBase
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase

from django.utils.translation import ugettext_lazy as _


class UserChangeForm(UserChangeFormBase):
    """Overrides the user update form."""

    class Meta(UserChangeFormBase.Meta):
        model = User


class UserCreationForm(UserCreationFormBase):
    """Overrides the user creation form."""

    email = forms.EmailField(label=_('Email'))

    error_message = UserCreationFormBase.error_messages.update({
        'duplicate_username': 'This username has already been taken.',
    })

    class Meta(UserCreationFormBase.Meta):
        model = User

    def clean_username(self):
        """Validates the username of a user."""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(self.error_messages['duplicate_username'])
        return username


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    """Defines the user admin behaviour."""

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Information'), {'fields': ('first_name', 'last_name', 'email', 'photo', 'phone_number', 'lang')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', 'full'),
            'fields': ('username', 'password1', 'password2', 'email'),
        }),
    )
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'is_superuser',
        'lang',
    ]
