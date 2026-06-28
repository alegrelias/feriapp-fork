"""Configuración del panel de administración para la app principal."""

from django.contrib import admin
from .models import Feria, Categoria, Emprendedor, Inscripcion, Visitante, Resenia, Sector

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

    search_fields = ('feria__nombre', 'fecha_inscripcion')

@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = list_display = ('nombre', 'apellido', 'email', 'usuario', 'fecha_registro')

    list_filter = ('fecha_registro', 'email')

    search_fields = ('nombre', 'fecha_registro')

@admin.register(Resenia)
class ReseniaAdmin(admin.ModelAdmin):
    list_display = ('visitante', 'feria', 'calificacion', 'comentario', 'fecha_resenia')

    list_filter = ('calificacion', 'feria__nombre', 'fecha_resenia')

    search_fields = ('calificacion', 'feria__nombre')

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('feria', 'edicion', 'nombre', 'capacidad_puestos', 'tiene_conexion_electrica')

    list_filter = ('feria__nombre', 'nombre', 'capacidad_puestos', 'tiene_conexion_electrica')

    search_fields = ('nombre', 'capacidad_puestos')