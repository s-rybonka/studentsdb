from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404


class ManagerRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'manager'
    permission_denied_message = 'Permission Denied'
    raise_exception = False

    def handle_no_permission(self):
        raise Http404()
