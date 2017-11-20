from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import ugettext as _
from django.views.generic import FormView, UpdateView

from accounts.models import Account
from cabinet.profile_.forms import SessionSettingsForm


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'cabinet/profile_/user_profile.html'
    model = Account
    fields = ['first_name', 'last_name', 'avatar', 'role']
    messages = {
        'success': _('Profile was updated')
    }

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.info(self.request, message=self.messages.get('success'))
        return reverse('cabinet:profile:personal-data')


class SessionSettingsView(LoginRequiredMixin, FormView):
    template_name = 'cabinet/profile_/session_settings.html'
    form_class = SessionSettingsForm
    success_url = reverse_lazy('cabinet:profile:session-settings')
    messages = {
        'success': _('Settings updated!')
    }

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        if self.request.user.is_authenticated:
            form.initial = {
                'timezone': self.request.user.timezone,
                'language': translation.get_language()
            }
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            account = Account.objects.get(pk=self.request.user.pk)
            account.timezone = form.cleaned_data['timezone']
            account.language = form.cleaned_data['language']
            account.save()
            translation.activate(language=form.cleaned_data['language'])
            messages.success(self.request, message=self.messages.get('success'))

        return super(SessionSettingsView, self).form_valid(form)
