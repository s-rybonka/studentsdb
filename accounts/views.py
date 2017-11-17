from allauth.account import views
from allauth.account.adapter import get_adapter


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
