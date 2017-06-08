from django.views import generic
from ..models.group import Group
from django.contrib.messages.views import SuccessMessageMixin
from ..forms import GroupForm
from django.shortcuts import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages
from ..util import get_current_group


# Manage Groups
class GroupsListView(generic.ListView):
    template_name = "cabinet_/groups/groups.html"
    model = Group
    paginate_by = 10

    def get_queryset(self):

        current_group = get_current_group(self.request)

        if current_group:
            queryset = Group.objects.filter(title=current_group)
        else:
            queryset = Group.objects.all()

        order_by = self.request.GET.get('order_by', '')
        if order_by in ('title', 'leader',):
            queryset = queryset.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                queryset = queryset.reverse()

        return queryset


class GroupsAddView(SuccessMessageMixin, generic.CreateView):
    template_name = 'cabinet_/groups/groups_add.html'
    model = Group
    form_class = GroupForm
    success_url = '/groups'
    success_message = _('%(title)s Added to group list!')


class GroupsEditView(SuccessMessageMixin, generic.UpdateView):
    model = Group
    template_name = 'cabinet_/groups/groups_edit.html'
    form_class = GroupForm
    success_url = '/groups'
    success_message = _('%(title)s Updated!')


class GroupsDeleteView(generic.DeleteView):
    template_name = 'cabinet_/groups/groups_delete_confirm.html'
    model = Group

    def get_success_url(self):
        return reverse('groups_list', messages.add_message(self.request, messages.SUCCESS, _('Group was deleted!')))
