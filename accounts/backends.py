from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Account


class SocialAuthBackend(ModelBackend):
    def authenticate(self, email=None,  **kwargs):
        if email is not None:
            try:
                user = Account.objects.get(email=email)
                if user:
                    return user
            except ObjectDoesNotExist:
                pass
