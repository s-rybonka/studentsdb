from django.views.generic import  FormView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib import messages
from django.utils import translation
from django.core.urlresolvers import reverse

from cabinet.profile_.forms import SessionSettingsForm
from accounts.models import Account


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'cabinet/profile_/user_profile.html'
    model = Account
    fields = ['username', 'first_name', 'last_name','avatar']

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('cabinet:profile:personal-data', messages.info(self.request, message=_('Profile was updated')))


class SessionSettingsView(LoginRequiredMixin, FormView):
    template_name = 'cabinet/profile_/session_settings.html'
    form_class = SessionSettingsForm
    success_url = reverse_lazy('cabinet:profile:session-settings')

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

            messages.add_message(
                self.request,
                messages.SUCCESS, _('Settings updated! Activated ({}) timezone.'.format(account.timezone)))

        return super(SessionSettingsView, self).form_valid(form)
