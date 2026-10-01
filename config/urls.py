"""Hoofdoverzicht van alle URL's."""

from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

admin.site.site_header = _("VDK working conditions – management")
admin.site.site_title = _("VDK management")

urlpatterns = [
    path("", TemplateView.as_view(template_name="start.html"), name="start"),
    path("beheer/", admin.site.urls),
]
