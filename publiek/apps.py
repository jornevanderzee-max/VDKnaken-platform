"""App publiek: medewerkerspagina, wervingspagina, PDF en tellers."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PubliekConfig(AppConfig):
    name = "publiek"
    verbose_name = _("Public pages")
