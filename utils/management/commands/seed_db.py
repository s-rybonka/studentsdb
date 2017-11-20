from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from accounts.models import Account
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from studentsdb import settings as psa

SOCIAL_AUTH_PROVIDERS = (

    (
        psa.FACEBOOK_PROVIDER_NAME,
        psa.FACEBOOK_APP_NAME,
        psa.FACEBOOK_APP_ID,
        psa.FACEBOOK_SECRET_KEY,
    ),
    (
        psa.GOOGLE_PROVIDER_NAME,
        psa.GOOGLE_APP_NAME,
        psa.GOOGLE_APP_ID,
        psa.GOOGLE_SECRET_KEY,
    ),
    (
        psa.TWITTER_PROVIDER_NAME,
        psa.TWITTER_APP_NAME,
        psa.TWITTER_APP_ID,
        psa.TWITTER_SECRET_KEY,
    ),

)


class Command(BaseCommand):
    help = 'Fill Database'

    def handle(self, *args, **options):
        # Create Django Group, for easier permission handling.
        for key in Account.ROLES:
            try:
                group = Group.objects.get(name=key[0])
                if group:
                    self.stdout.write(self.style.ERROR('Group "%s" already exist' % group.name))
            except Group.DoesNotExist:
                group = Group.objects.create(name=key[0])
                self.stdout.write(self.style.SUCCESS('Group: "%s" created' % group.name))

        domain_name = psa.DOMAIN_NAME

        # create social apps
        for s in SOCIAL_AUTH_PROVIDERS:
            try:
                provider = SocialApp.objects.get(provider=s[0])

                if provider:
                    self.stdout.write(self.style.ERROR(
                        'Social App {} already exist'.format(s[1])))
            except SocialApp.DoesNotExist:
                social_app = SocialApp.objects.create(
                    provider=s[0],
                    name=s[1],
                    client_id=s[2],
                    secret=s[3])
                site = Site.objects.get_by_natural_key(
                    domain=domain_name)
                social_app.sites.add(site)
                self.stdout.write(self.style.SUCCESS(
                    'Social App {} successfully created'.format(s[1])))