"""Gebruikers van het platform: superbeheerders en bedrijfsbeheerders.

Een gebruiker logt in met het e-mailadres. Welke bedrijven iemand mag
beheren, komt in stap 1 via het model Lidmaatschap.
"""

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class GebruikerManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **velden):
        if not email:
            raise ValueError("Een gebruiker heeft een e-mailadres nodig.")
        gebruiker = self.model(email=self.normalize_email(email).lower(), **velden)
        gebruiker.set_password(password)
        gebruiker.save(using=self._db)
        return gebruiker

    def create_superuser(self, email, password=None, **velden):
        velden["is_superuser"] = True
        return self.create_user(email, password, **velden)


class Gebruiker(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    naam = models.CharField(_("name"), max_length=150, blank=True)
    is_active = models.BooleanField(_("active"), default=True)
    # Overschrijft het veld uit PermissionsMixin; dit is het vinkje "superbeheerder".
    is_superuser = models.BooleanField(
        _("super administrator"),
        default=False,
        help_text=_("Super administrators manage the central VDKnaken, all companies and all accounts."),
    )
    aangemaakt_op = models.DateTimeField(_("created at"), auto_now_add=True)

    # last_login en het wachtwoord komen uit AbstractBaseUser.

    objects = GebruikerManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["email"]

    def __str__(self):
        return self.email

    @property
    def is_superbeheerder(self):
        return self.is_superuser

    @property
    def is_staff(self):
        # Alleen superbeheerders mogen in de Django-beheeromgeving (tot stap 9).
        return self.is_superuser
