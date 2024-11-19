from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from apps.users.manager import CustomUserManager
from apps.common.models import BaseModel


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(max_length=255, unique=True, blank=False, null=False)
    full_name = models.CharField(_('full name'), max_length=255, blank=True, null=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'