# -*- coding: utf-8 -*-

import logging
from django import forms

from apps.accounts.models.user import User

from django.contrib.auth import password_validation

from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class ResetPasswordForm(forms.Form):
    """Validates the reset password process."""

    password1 = forms.CharField()
    password2 = forms.CharField()

    def clean_password2(self):
        """Validates two passwords."""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('Passwords Mismatch'))
        return password2


class UserCreationForm(forms.ModelForm):
    """Validates the user creation process."""

    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        strip=False,
        help_text=_('Put your password again'),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']

    def clean_password2(self):
        """Validates two passwords and username."""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('Passwords Mismatch'))

        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        """Saves the user data."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
