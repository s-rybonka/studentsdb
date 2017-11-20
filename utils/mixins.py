from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.utils.translation import gettext_lazy as _


class ManagerRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'accounts.manager'
    permission_denied_message = 'Permission Denied'
    raise_exception = False

    def handle_no_permission(self):
        return HttpResponseForbidden(_('Permission denied'))


class GuestRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'accounts.guest'
    permission_denied_message = 'Permission Denied'
    raise_exception = False

    def handle_no_permission(self):
        return HttpResponseForbidden(_('Permission denied'))