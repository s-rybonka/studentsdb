import rules
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        # user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=30, unique=True, null=True, verbose_name=_('Nicname'))

    first_name = models.CharField(max_length=30, null=True, verbose_name=_('Name'))

    last_name = models.CharField(max_length=30, null=True, verbose_name=_('Surname'))
    is_email_confirmed = models.BooleanField(verbose_name='Email confirmed', default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    data_joined = models.DateTimeField(verbose_name='Date joined', auto_now_add=True, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin or rules.has_perm(perm, self, obj)

    def has_perms(self, perms, obj=None):
        "Does the user have a specific permission?"

        return self.is_admin or all(rules.has_perm(perm, self, obj) for perm in perms)

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return self.is_admin or rules.has_perm(app_label, self)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class AccountRoles(models.Model):
    account = models.ForeignKey('accounts.Account', verbose_name='Account', related_name='account_roles')
    is_manager = models.BooleanField(default=False)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return  rules.has_perm(perm, self, obj)

    def has_perms(self, perms, obj=None):
        "Does the user have a specific permission?"

        return  all(rules.has_perm(perm, self, obj) for perm in perms)

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return rules.has_perm(app_label, self)
