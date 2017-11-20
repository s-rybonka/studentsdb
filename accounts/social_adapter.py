from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from accounts.models import Account
from allauth.account.utils import perform_login


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """Return user's social profile

    If user exist in django app, associate social account
    to this profile, else create new one
    """
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if user.id:
            return
        try:
            customer = Account.objects.get(email=user.email)
            sociallogin.state['process'] = 'connect'
            perform_login(request, customer, 'none')
        except Account.DoesNotExist:
            pass
