"""Configuración del panel de administración para la app principal."""

from django.contrib import admin
from .models import Feria, Categoria, Emprendedor, Inscripcion, Visitante, Resenia, Sector


class SectorInline(admin.TabularInline):
    model = Sector
    extra = 1

@admin.register(Feria)
class FeriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'fecha_inicio', 'fecha_fin', 'activa')

    list_filter = ('activa', 'categoria')

    search_fields = ('nombre', 'ubicacion')

    fieldsets = (
        ('Informacion Principal', {
            'fields': ('nombre', 'categoria', 'ubicacion')
        }),
        ('Fechas y Planificacion',{
            'fields': ('fecha_inicio', 'fecha_fin', 'activa')
        })
    )

    inlines = [SectorInline]

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

    list_filter = ('nombre',)

    search_fields = ('nombre', 'descripcion')

    fieldsets = (
        ('Informacion Principal', {
            'fields': ('nombre', 'descripcion')
        }),
    )

class InscripcionInline(admin.TabularInline):
    model = Inscripcion
    extra = 0
    can_delete = False
    readonly_fields = ('feria', 'numero_puesto', 'fecha_inscripcion', 'estado', 'registrado_por')

@admin.register(Emprendedor)
class EmprendedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'rubro', 'telefono', 'usuario')

    list_filter = ('email', 'telefono')

    search_fields = ('apellido', 'email')

    fieldsets = (
        ('Datos Personales', {
            'fields': ('nombre', 'apellido', 'email','telefono', 'usuario')
        }),
        ('Informacion de ferias',{
            'fields': ('rubro',)
        })
    )

    inlines = [InscripcionInline]


#En Django, los campos automáticos no se muestran en los formularios de edición por defecto
@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('emprendedor', 'feria', 'numero_puesto', 'fecha_inscripcion', 'estado', 'registrado_por')
    list_filter = ('fecha_inscripcion', 'estado')
    search_fields = ('feria__nombre', 'emprendedor__apellido') 

    # Habilitamos que la fecha se pueda ver en el formulario
    readonly_fields = ('fecha_inscripcion',)

    fieldsets = (
        ('Información Principal', {
            'fields': ('emprendedor', 'feria')
        }),
        ('Estado y Asignación', {
            'fields': ('estado', 'numero_puesto'),
            'description': '⚠️ Las inscripciones confirmadas deben tener un número de puesto asignado.'
        }),
        ('Datos de Auditoría', {
            'fields': ('registrado_por', 'fecha_inscripcion'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'usuario', 'fecha_registro')

    list_filter = ('fecha_registro', 'email')

    search_fields = ('nombre', 'email')

    fieldsets = (
        ('Datos Personales', {
            'fields': ('nombre', 'apellido', 'email', 'usuario')
        }),
        ('Datos de Auditoría', {
            'fields': ('fecha_registro',)
        }),
    )

@admin.register(Resenia)
class ReseniaAdmin(admin.ModelAdmin):
    list_display = ('visitante', 'feria', 'calificacion', 'comentario', 'fecha_resenia')
    list_filter = ('calificacion', 'feria__nombre', 'fecha_resenia')

    search_fields = ('feria__nombre', 'visitante__nombre', 'visitante__apellido')

    readonly_fields = ('fecha_resenia',)

    fieldsets = (
        ('Contexto', {
            'fields': ('visitante', 'feria'),
            'description': 'Indica qué visitante está evaluando qué feria.'
        }),
        ('Evaluación', {
            'fields': ('calificacion', 'comentario'),
        }),
        ('Metadatos', {
            'fields': ('fecha_resenia',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('feria', 'edicion', 'nombre', 'capacidad_puestos', 'tiene_conexion_electrica')

    list_filter = ('feria__nombre', 'nombre', 'capacidad_puestos', 'tiene_conexion_electrica')

    search_fields = ('nombre', 'edicion')

    fieldsets = (
        ('Informacion Principal', {
            'fields': ('edicion', 'nombre', 'feria')
        }),
        ('Datos del Sector', {
            'fields': ('capacidad_puestos', 'tiene_conexion_electrica'),
        })
    )