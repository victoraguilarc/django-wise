# -*- coding: utf-8 -*-

from apps.accounts.models import User


class UserService:
    """Contains all utility methods to help user precesses."""

    @classmethod
    def update_profile(cls, user, changes):
        """Updates some fields of the user instance."""
        if 'username' in changes:
            user.username = changes.get('username')

        if 'first_name' in changes:
            user.first_name = changes.get('first_name')

        if 'last_name' in changes:
            user.last_name = changes.get('last_name')

        if 'photo' in changes:
            if changes.get('photo') is not None:
                photo = changes.get('photo')
                user.photo.save(photo.name, photo)
        user.save()
        user.refresh_from_db()

        return user

    @classmethod
    def register_new_user(cls, user_data, is_active=False):
        """Creates an user instance."""
        plain_password = user_data.pop('password')

        if 'username' not in user_data and 'email' in user_data:
            user_data['username'] = user_data['email']

        user = User(**user_data)
        user.is_active = is_active
        user.set_password(plain_password)
        user.save()

        return user

    @classmethod
    def create_or_update_for_social_networks(cls, email, first_name, last_name):
        """Creates or updates and user instance."""
        user, created = User.objects.update_or_create(
            email=email, defaults={
                'first_name': first_name,
                'last_name': last_name,
                'is_active': True,
            },
        )
        user.save()

        return user
