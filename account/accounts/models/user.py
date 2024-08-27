from django.db import models
from django.core.validators import RegexValidator
    
from django.forms.models import model_to_dict

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _

from django.db import models

from . import role
from .utils import TimeStamp


class UserManager(BaseUserManager):
    """ User manager """

    def _create_user(self, email, password=None, **extra_fields):
        
        """Creates and returns a new user using an email address"""
        if not email:  # check for an empty email
            raise AttributeError("User must set an email address")
        else:  # normalizes the provided email
            email = self.normalize_email(email)

        # if not role:  # check for an empty role
           # raise ValueError("User must set an Role")
        
        # Oauth
        # if not password:  # check for password
        #     raise ValueError("User must set an password")
        
        # create user

        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # hashes/encrypts password
        user.save(using=self._db)  # safe for multiple databases
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Creates and returns a new user using an email address"""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
        
    def create_staffuser(self, email, password=None, **extra_fields):
        """Creates and returns a new staffuser using an email address"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and returns a new superuser using an email address"""
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password,**extra_fields)

# User Base

import uuid

PLATFORM_CHOICES = (
    ("email", "Email"),
    ("google", "Google"),
    ("facebook", "Facebook"),
)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Login
    email = models.EmailField(
        _("Email Address"),
        max_length=255,
        unique=True,
        help_text="Ex: example@example.com",
        error_messages={
            "unique": "A User with this email address already exists."
        }
    )

    # Platform
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default="email")

    # Django Stuffs
    is_active = models.BooleanField(_("Active status"), default=True)
    is_staff = models.BooleanField(_("Staff status"), default=False)
    created_at = models.DateTimeField(_("Date Joined"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Last Updated"), auto_now=True)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"
    
    class Meta:
        db_table = 'user'

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'user_accounts'

    @property
    def get_permissions(self):
        try:
            return self.userrole.get_permissions
        except Exception as e:
            return []
        
    @property
    def get_permissions_check(self):
        check_permission_format = {}
        
        for permission in self.get_permissions:
            check_permission_format[permission["name"]] = permission["value"]

        return check_permission_format
    
    @property
    def check_vendor_profile(self):
        if hasattr(self, 'vendorprofile'):
            vendor_profile_dict = model_to_dict(self.vendorprofile)
            
            # Remove the 'profile_image' if it has no file associated
            if self.vendorprofile.profile_image:
                vendor_profile_dict['profile_image'] = self.vendorprofile.profile_image.url
            else:
                vendor_profile_dict['profile_image'] = None

            return vendor_profile_dict
        return None
    
    @property
    def check_client_profile(self):
        if hasattr(self, 'clientprofile'):
            modified_data = model_to_dict(self.clientprofile)

            return modified_data
        return None


    @property
    def has_admin_profile(self):
        return hasattr(self, 'admin_profile')
