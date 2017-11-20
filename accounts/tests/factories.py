import factory
from accounts.models import Account
from django.contrib.auth.hashers import make_password


class AccountFactory(factory.DjangoModelFactory):
    """
    Account Factory
    """
    class Meta:
        model = Account

    first_name = factory.Sequence(lambda n: 'john%s' % n)
    last_name = factory.Sequence(lambda n: 'dou%s' % n)
    email = factory.LazyAttribute(lambda o: '%s@example.com' % o.first_name)
    password = make_password('1')
