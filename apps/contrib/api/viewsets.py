# -*- coding: utf-8 -*-

from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet


class PermissionlMixin(object):
    """Views permission mixin.

    Mixed permission base model allowing for action level
    permission control. Subclasses may define their permissions
    by creating a 'permission_classes_by_action' variable.

    Example:
    permissions_by_action = {'list': [AllowAny], 'create': [IsAdminUser]}

    """

    permissions_by_action = {}

    def get_permissions(self):
        """Returns permissions calculation."""
        try:
            return [permission() for permission in self.permissions_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class ModelListViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    """Enables list method with permissions."""


class ModelUpdateListViewSet(  # noqa: WPS215
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """Enables list and update methods with permissions."""


class ModelRetrieveListViewSet(  # noqa: WPS215
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """Enables list and retrieve methods with permissions."""


class ModelRetrieveUpdateListViewSet(  # noqa: WPS215
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """Enables retrieve and update methods with permissions."""


class ModelCreateRetrieveListViewSet(  # noqa: WPS215
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """Enables list, create and retrieve methods with permissions."""


class ModelCreateListViewSet(  # noqa: WPS215
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """Enables list and createe methods with permissions."""


class PermissionModelViewSet(PermissionlMixin, ModelViewSet):
    """Enables all modeel methods with permissions."""


class PermissionViewSet(PermissionlMixin, GenericViewSet):
    """Enables standar view methods with permissions."""
