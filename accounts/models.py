import rules
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from timezone_field import TimeZoneField


class UserManager(BaseUserManager):
    """
    Custom User Manager
    """

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
    """
    Custom User model, named Account
    """
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        max_length=30, unique=True, null=True, verbose_name=_('Nickname'))
    first_name = models.CharField(
        max_length=30, null=True, verbose_name=_('Name'))
    last_name = models.CharField(
        max_length=30, null=True, verbose_name=_('Surname'))
    avatar = models.ImageField(upload_to='media')
    is_email_confirmed = models.BooleanField(verbose_name='Email confirmed', default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    timezone = TimeZoneField(verbose_name=_('Time zone'), default="UTC")
    language = models.CharField(max_length=20)
    data_joined = models.DateTimeField(verbose_name='Date joined', auto_now_add=True, null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        """ Get user's full name """
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        """ Get user nickname """
        return self.username

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """ Does the user have a specific permission """
        return self.is_admin or rules.has_perm(perm, self, obj)

    def has_perms(self, perms, obj=None):
        """ Does the user have a specific permission """
        return self.is_admin or all(rules.has_perm(perm, self, obj) for perm in perms)

    def has_module_perms(self, app_label):
        """ Does the user have permissions to view the app `app_label` """
        return self.is_admin or rules.has_perm(app_label, self)

    # TODO rename to is_admin
    @property
    def is_staff(self):
        """ Is the user a member admin """
        return self.is_admin


