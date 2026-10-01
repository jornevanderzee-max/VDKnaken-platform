"""App bedrijven: editor voor bedrijfsbeheerders, concept en publiceren."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BedrijvenConfig(AppConfig):
    name = "bedrijven"
    verbose_name = _("Companies")
