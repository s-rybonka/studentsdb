from allauth.account import views
from allauth.account.adapter import get_adapter
from django.views.generic import ListView, DetailView
from accounts.models import Account
from django.contrib.auth.mixins import LoginRequiredMixin

class SignUpView(views.SignupView):
    template_name = 'account/signup.html'


class SignInView(views.LoginView):
    template_name = 'account/login.html'


class SignOutView(views.LogoutView):
    template_name = 'account/logout.html'

    def logout(self):
        """
        Django allauth method.
        Successful logout message had been removed.
        :return: None
        """
        adapter = get_adapter(self.request)
        adapter.logout(self.request)


class AccountListView(LoginRequiredMixin, ListView):
    """
    Account list view.
    Represents registered on site users.
    """
    template_name = 'account/account_list.html'
    model = Account
    paginate_by = 10


class AccountDetailView(DetailView):
    template_name = 'account/account_detail.html'
    model = Account