"""Configuración del panel de administración para la app principal."""

from django.contrib import admin
from .models import Feria

# TODO: reemplazar por @admin.register con list_display, list_filter, search_fields
admin.site.register(Feria)
