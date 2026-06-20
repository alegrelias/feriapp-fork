"""Configuración del panel de administración para la app principal."""

from django.contrib import admin
from .models import Feria, Categoria, Emprendedor, Inscripcion 

# TODO: reemplazar por @admin.register con list_display, list_filter, search_fields
@admin.register(Feria)
class FeriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'fecha_inicio', 'fecha_fin', 'activa')

    list_filter = ('activa', 'categoria')

    search_fields = ('nombre', 'ubicacion')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

    list_filter = ('nombre',)

    search_fields = ('nombre', 'descripcion')

@admin.register(Emprendedor)
class EmprendedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'rubro', 'telefono', 'usuario')

    list_filter = ('email', 'telefono')

    search_fields = ('apellido', 'email')

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('emprendedor', 'feria', 'numero_puesto', 'fecha_inscripcion', 'estado', 'registrado_por')

    list_filter = ('fecha_inscripcion', 'numero_puesto')

    search_fields = ('feria', 'fecha_inscripcion')