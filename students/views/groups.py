from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse
from django.utils.translation import ugettext as _
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from ..forms import GroupForm
from ..models.group import Group
from ..util import get_current_group


class GroupsListView(LoginRequiredMixin, generic.ListView):
    template_name = "cabinet/groups/groups.html"
    model = Group
    paginate_by = 10
    filter_reverse_indicator = 1

    def get_queryset(self):
        current_group = get_current_group(self.request)
        # If group exist
        if current_group:
            queryset = Group.objects.filter(title=current_group)
        else:
            queryset = Group.objects.all()
        # Get parameters from GET request
        order_by = self.request.GET.get('order_by', '')
        if order_by in ('title', 'leader',):
            queryset = queryset.order_by(order_by)
            if self.request.GET.get('reverse', '') == self.filter_reverse_indicator:
                queryset = queryset.reverse()
        return queryset


class GroupsAddView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = 'cabinet/groups/groups_add.html'
    model = Group
    form_class = GroupForm
    success_url = reverse_lazy('groups_list')
    success_message = _('%(title)s Added to group list!')


class GroupsEditView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Group
    template_name = 'cabinet/groups/groups_edit.html'
    form_class = GroupForm
    success_url = reverse_lazy('groups_list')
    success_message = _('%(title)s Updated!')


class GroupsDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'cabinet/groups/groups_delete_confirm.html'
    model = Group

    def get_success_url(self):
        return reverse('groups_list', messages.add_message(self.request, messages.SUCCESS, _('Group was deleted!')))
