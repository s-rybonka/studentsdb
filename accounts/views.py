from allauth.account import views


class SignUpView(views.SignupView):
    template_name = 'account/signup.html'


class SignInView(views.LoginView):
    template_name = 'account/login.html'


class SignOutView(views.LogoutView):
    template_name = 'account/logout.html'


