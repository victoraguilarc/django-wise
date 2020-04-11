# -*- coding: utf-8 -*-

from rest_framework.permissions import BasePermission, IsAuthenticated


class IsOwner(BasePermission):
    """Checks if the object's owner is a certain user."""

    def has_object_permission(self, request, view, obj):
        """Checks the object permissions."""
        return obj.user == request.user


class IsSuperUser(IsAuthenticated):
    """Checks if the user has permissions as superuser."""

    def has_permission(self, request, view, obj=None):
        """Checks if the user has permissions."""
        return request.user and request.user.is_authenticated and request.user.is_superuser
