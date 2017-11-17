from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class ManagerRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'accounts.manager'
    permission_denied_message = 'Permission Denied'
    raise_exception = False


class GuestRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'accounts.guest'
    permission_denied_message = 'Permission Denied'
    raise_exception = False