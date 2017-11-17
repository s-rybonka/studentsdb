from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import Permission
from django.contrib.auth.models import PermissionsMixin
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from timezone_field import TimeZoneField


class UserManager(BaseUserManager):
    """
    Custom User Manager
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model, named Account
    """

    MANAGER = 'manager'
    GUEST = 'guest'
    ROLES = Choices(
        (MANAGER, 'MANAGER', _('Manager')),
        (GUEST, 'GUEST', _('Guest')),
    )
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    avatar = models.ImageField(upload_to='media')
    role = models.CharField(choices=ROLES, max_length=100, verbose_name=_('Account type'), default=ROLES.GUEST)
    is_email_confirmed = models.BooleanField(verbose_name='Email confirmed', default=False)
    timezone = TimeZoneField(verbose_name=_('Time zone'), default="UTC", )
    language = models.CharField(max_length=20)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def is_manager(self):
        return self.role == self.ROLES.MANAGER

    @property
    def is_guest(self):
        return self.role == self.ROLES.GUEST

    @property
    def member_role(self):
        if self.role:
            return self.role.upper()

    def get_full_name(self):
        """
        Get user's full name.
        If can't get full name, we will get username
         """
        if self.first_name and self.last_name:
            return "{} {}".format(self.first_name, self.last_name)
        elif self.username:
            return self.username

    def get_short_name(self):
        """ Get user nickname """
        return self.first_name

    def __str__(self):
        return self.email

    def create_custom_permission(self, role_type):
        """
        Create custom permission for specific user role.
        Will be used in PermissionRequiredMixin.

        :param role_type:
        :return: str: permission ('manager', 'guest')
        """
        content_type = ContentType.objects.get_or_create(
            model="", app_label=self._meta.app_label
        )
        permission = Permission.objects.get_or_create(
            codename=role_type,
            name=role_type,
            content_type=content_type[0],
        )
        return permission[0]

    def set_custom_user_permission(self):
        """
        Add permission to user.
        Remove old permission.

        :return: None
        """
        # TODO Maybe need refactor this part in the future.
        self.remove_permissions(self.GUEST, self.MANAGER)
        if self.role == self.MANAGER:
            is_manager_permission = self.create_custom_permission(self.MANAGER)
            self.user_permissions.add(is_manager_permission)
        elif self.role == self.GUEST:
            is_guest_permission = self.create_custom_permission(self.GUEST)
            self.user_permissions.add(is_guest_permission)

    def remove_permissions(self, *args):
        custom_user_permissions = Permission.objects.filter(codename__in=args)
        if custom_user_permissions:
            for permission in custom_user_permissions:
                self.user_permissions.remove(permission)

    def save(self, *args, **kwargs):
        # TODO Add condition, check if role field was affected.
        instance = super().save(*args, **kwargs)
        self.set_custom_user_permission()
        return instance