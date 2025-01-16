from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, telegram_id, username, first_name='', last_name='', password=None, **extra_fields):
        if not telegram_id:
            raise ValueError("The Telegram ID is required.")

        user = self.model(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_id, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(telegram_id, username, password=password, **extra_fields)


class User(AbstractBaseUser):
    telegram_id = models.CharField(max_length=50, unique=True, verbose_name=_("Telegram ID"))
    username = models.CharField(max_length=150, unique=True, verbose_name=_("Username"))
    first_name = models.CharField(max_length=150, blank=True, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=150, blank=True, verbose_name=_("Last Name"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Staff status"))
    is_superuser = models.BooleanField(default=False, verbose_name=_("Superuser status"))

    objects = UserManager()

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.telegram_id})"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
