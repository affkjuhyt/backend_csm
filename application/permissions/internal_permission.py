from django.utils.translation import ugettext as _
from rest_framework import permissions


class InternalPermission(permissions.BasePermission):
    @property
    def app_label(self) -> str:
        raise NotImplementedError(_('app_label must be defined'))

    def _get_view_permissions(self, view):
        assert hasattr(view, 'permission_codes') is True, (
            'Cannot apply AdminUserPermission on a view that '
            'does not set `.permission_codes` '
        )

        permission_codes = view.permission_codes
        if isinstance(permission_codes, str):
            # If permission_codes actions is not specified, this permission
            # will be use for all actions
            return permission_codes
        elif isinstance(permission_codes, dict):
            return permission_codes.get(view.action)
        raise ValueError(_("permission codes invalid"))

    def has_permission(self, request, view):
        perm = self._get_view_permissions(view=view)
        if perm:
            result = request.user.has_perm('{}.{}'.format(self.app_label, perm))
            return result
        else:
            return True
