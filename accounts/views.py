import uuid
import requests
from requests import Request
from allauth.account import views
from allauth.account.adapter import get_adapter
from django.views.generic import ListView, DetailView
from django.http import Http404
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.conf import settings
from accounts.models import Account
from django.shortcuts import redirect
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


def github_connect(request):
    """
    Request to GITHUB for getting grants.
    :param request:
    :return: grants.
    """
    state = str(uuid.uuid4())
    request.session['github_auth_state'] = state
    params = {
        'client_id': settings.GITHUB_APP_ID,
        'scope': 'user:email',
        'state': state
    }
    github_auth_url = 'https://github.com/login/oauth/authorize'
    r = Request('GET', url=github_auth_url, params=params).prepare()
    return redirect(r.url)


def github_callback(request):
    """
    Listen for GITHUB response.
    :param request:
    :return:
    """
    # Get original from session
    original_state = request.session.get('github_auth_state')
    if not original_state:
        raise Http404
    del(request.session['github_auth_state'])

    state = request.GET.get('state')
    code = request.GET.get('code')

    if not state and not code:
        raise Http404
    if original_state != state:
        raise Http404

    # If all right and we have grant,
    # we ready to request access_token from GITHUB.

    params = {
        'client_id': settings.GITHUB_APP_ID,
        'client_secret': settings.GITHUB_APP_SECRET_KEY,
        'code': code
    }
    headers = {'accept': 'application/json'}
    url = 'https://github.com/login/oauth/access_token'
    r = requests.post(url=url, params=params, headers=headers)

    if not r.ok:
        raise Http404

    data = r.json()
    access_token = data.get('access_token')

    # Prepare data for getting user credentials from github.
    headers = {
        'authorization': 'token %s' % access_token
    }
    # Make request to github.
    r = requests.get('https://api.github.com/user', headers=headers)
    user_data = r.json()

    # User email can be unavailable form github, according to profile settings.
    # Get or create user in local DB.

    # TODO refactor for production.
    # Need adapt it for many Social networks, keep it in one place.
    # Check if user has token, if user already exist etc.
    try:
        user = Account.objects.get(email=user_data.get('email'))
    except Account.DoesNotExist:
        user = Account.objects.create(email=user_data.get('email'), github_token=access_token)
    user = authenticate(email=user.email)
    if user and user.is_authenticated():
        login(request=request, user=user)
    return redirect('home-page')

# TODO read allauth doc.
# TODO facebook auth via js SDK.
# TODO facebook login custom.
# TODO read https://github.com/noamsu/django-facebook-connect
# TODO Add password change possibility.