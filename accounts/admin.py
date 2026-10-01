"""Gebruikers beheren in de Django-beheeromgeving (tot het portaal in stap 9 af is)."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

from .models import Gebruiker


class GebruikerAanmaakFormulier(AdminUserCreationForm):
    class Meta:
        model = Gebruiker
        fields = ["email", "naam"]


class GebruikerWijzigFormulier(UserChangeForm):
    class Meta:
        model = Gebruiker
        fields = "__all__"


@admin.register(Gebruiker)
class GebruikerAdmin(UserAdmin):
    form = GebruikerWijzigFormulier
    add_form = GebruikerAanmaakFormulier

    list_display = ["email", "naam", "is_superuser", "is_active", "last_login"]
    list_filter = ["is_superuser", "is_active"]
    search_fields = ["email", "naam"]
    ordering = ["email"]
    readonly_fields = ["last_login", "aangemaakt_op"]
    filter_horizontal = []

    fieldsets = [
        (None, {"fields": ["email", "naam", "password"]}),
        (_("Rights"), {"fields": ["is_active", "is_superuser"]}),
        (_("Dates"), {"fields": ["last_login", "aangemaakt_op"]}),
    ]
    add_fieldsets = [
        (None, {"classes": ["wide"], "fields": ["email", "naam", "password1", "password2"]}),
    ]
