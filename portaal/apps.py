"""App portaal: superbeheerdersportaal en export."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PortaalConfig(AppConfig):
    name = "portaal"
    verbose_name = _("Portal")
