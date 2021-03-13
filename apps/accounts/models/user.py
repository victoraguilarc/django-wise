# -*- coding: utf-8 -*-

# Built in

from django.db import models
from django.conf import settings
from django.core import validators
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from phonenumber_field.modelfields import PhoneNumberField

from apps.contrib.utils.files import clean_static_url

from django.contrib.auth.models import AbstractUser

from django.utils.translation import ugettext_lazy as _

REQUIRED_FIELDS = getattr(settings, 'PROFILE_REQUIRED_FIELDS', ['email'])


class User(AbstractUser):
    """Represents the user of the platform."""

    USERNAME_FIELD = 'username'

    username = models.CharField(
        _('username'),
        max_length=50,
        unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _(
                    'Enter a valid username. This value may contain only ' +
                    'letters, numbers and @/./+/-/_ characters.',
                ),
            ),
        ],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
        db_index=True,
    )

    email = models.EmailField(
        _('Email Address'),
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
        unique=True,
        db_index=True,
    )

    first_name = models.CharField(
        verbose_name=_('First Name'),
        max_length=100,
        blank=True, null=True,
    )

    last_name = models.CharField(
        verbose_name=_('Last Name'),
        max_length=150,
        blank=True, null=True,
    )

    photo = ProcessedImageField(
        verbose_name=_('Photo'),
        upload_to='profiles/%Y/%m/%d',
        processors=[ResizeToFill(350, 350)],
        format='PNG',
        options={'quality': 80},
        blank=True, null=True,
    )

    phone_number = PhoneNumberField(
        verbose_name=_('Phone Number'),
        null=True, blank=True,
    )

    lang = models.CharField(
        verbose_name=_('Language'),
        choices=settings.LANGUAGES,
        max_length=6,
        default='en',
    )

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.username is None or self.username.strip() == '':
            self.username = self.email
        super().save(*args, **kwargs)

    def change_password(self, new_password):
        self.set_password(new_password)
        self.save()

    @property
    def full_name(self):
        full_name = '{0} {1}'.format(self.first_name, self.last_name)
        return full_name.strip()

    @property
    def photo_url(self):
        return clean_static_url(self.photo.url) if self.photo else None

    @property
    def recipient_name(self):
        if self.first_name:
            return self.first_name
        return self.username

    @property
    def has_valid_phone_number(self):
        return self.phone_number is not None

    class Meta:
        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        unique_together = ('email', 'phone_number')
        app_label = 'accounts'
