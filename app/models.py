"""Modelos de dominio para la aplicación de ferias."""

from __future__ import annotations

from django.db import models
from app.base_models import ValidableModel
#Importo esta clase que permite usar la clase "User" provista por Django
from django.contrib.auth.models import User


class Feria(ValidableModel):#<- ya no heredamos de models.Models sino de ValidableModel
    """Representa una feria con su período, ubicación y capacidad disponible."""

    nombre = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    ubicacion = models.CharField(max_length=200)
    capacidad_puestos = models.PositiveIntegerField()
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["fecha_inicio"]

    def __str__(self):
        """Retorna una representación legible de la feria."""
        return self.nombre

    def puestos_ocupados(self):
        """Retorna la cantidad de inscripciones confirmadas."""
        # Mientras Inscripcion no exista, no hay relaciones para contar.
        if not hasattr(self, "inscripcion_set"):
            return 0
        return self.inscripcion_set.filter(estado="confirmada").count()

    def puestos_disponibles(self):
        """Retorna los puestos libres."""
        return self.capacidad_puestos - self.puestos_ocupados()

    def tiene_lugar(self):
        """Retorna True si quedan puestos disponibles."""
        return self.puestos_disponibles() > 0

    @classmethod
    def validate(cls, **kwargs) -> list[str]:
        """
        Valida los datos de la feria. Retorna una lista de errores.
        Si la lista está vacía, los datos son válidos.
        """
        errors = []

        # Extracción segura de los argumentos pasados por la vista o tests
        nombre = kwargs.get('nombre', '').strip() if kwargs.get('nombre') else ''
        categoria = kwargs.get('categoria', '').strip() if kwargs.get('categoria') else ''
        ubicacion = kwargs.get('ubicacion', '').strip() if kwargs.get('ubicacion') else ''
        capacidad_puestos = kwargs.get('capacidad_puestos')
        fecha_inicio = kwargs.get('fecha_inicio')
        fecha_fin = kwargs.get('fecha_fin')

        if not nombre or not nombre.strip():
            errors.append("El nombre es obligatorio.")

        if not categoria or not categoria.strip():
            errors.append("La categoría es obligatoria.")

        if not ubicacion or not ubicacion.strip():
            errors.append("La ubicación es obligatoria.")

        if capacidad_puestos is None or capacidad_puestos <= 0:
            errors.append("La capacidad de puestos debe ser mayor a cero.")

        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            errors.append("La fecha de fin no puede ser anterior a la fecha de inicio.")

        return errors

    # =========================================================================
    # NOTA PARA EL GRUPO: Los métodos 'new' y 'update' han sido comentados
    # porque ahora se heredan de forma genérica y automatizada desde la 
    # clase abstracta 'ValidableModel' (ubicada en app/base_models.py).
    #
    # Al heredar de ValidableModel, NINGUNO  necesita volver a 
    # escribir 'new' ni 'update' en sus respectivos modelos (User, Inscripcion, etc).
    # Solo debemos preocuparnos por escribir el método 'validate' de cada clase.
    # =========================================================================

    # @classmethod
    # def new(cls, **kwargs):
    #     """
    #     YA NO ES NECESARIO: ValidableModel ya maneja este flujo:
    #     1. Llama a cls.validate(**kwargs)
    #     2. Si hay errores, retorna (None, errors)
    #     3. Si está limpio, ejecuta cls.objects.create(**kwargs) y retorna (instancia, [])
    #     """
    #     pass

    # def update(self, **kwargs):
    #     """
    #     YA NO ES NECESARIO: ValidableModel ya maneja este flujo:
    #     1. Llama a self.__class__.validate(**kwargs)
    #     2. Si falla, frena y retorna los errores.
    #     3. Si pasa, mapea los cambios con setattr() en memoria y ejecuta self.save()
    #     """
    #     pass
    
    # @classmethod
    # def new(
    #     cls, nombre, categoria, fecha_inicio, fecha_fin, ubicacion, capacidad_puestos
    # ):
    #     """
    #     Crea y persiste una nueva feria si los datos son válidos.
    #     Retorna (instancia, errors). Si hay errores, instancia es None.
    #     """
    #     errors = cls.validate(
    #         nombre, categoria, fecha_inicio, fecha_fin, ubicacion, capacidad_puestos
    #     )
    #     if errors:
    #         return None, errors

    #     feria = cls.objects.create(
    #         nombre=nombre.strip(),
    #         categoria=categoria.strip(),
    #         fecha_inicio=fecha_inicio,
    #         fecha_fin=fecha_fin,
    #         ubicacion=ubicacion.strip(),
    #         capacidad_puestos=capacidad_puestos,
    #     )
    #     return feria, []

    # def update(
    #     self, nombre, categoria, fecha_inicio, fecha_fin, ubicacion, capacidad_puestos
    # ):
    #     """
    #     Actualiza los datos de la feria si los datos son válidos.
    #     Retorna una lista de errores. Si está vacía, la actualización fue exitosa.
    #     """
    #     errors = self.__class__.validate(
    #         nombre, categoria, fecha_inicio, fecha_fin, ubicacion, capacidad_puestos
    #     )
    #     if errors:
    #         return errors

    #     self.nombre = nombre.strip()
    #     self.categoria = categoria.strip()
    #     self.fecha_inicio = fecha_inicio
    #     self.fecha_fin = fecha_fin
    #     self.ubicacion = ubicacion.strip()
    #     self.capacidad_puestos = capacidad_puestos
    #     self.save()
    #     return []

    # TODO: Agregar los siguientes modelos:
    # class Categoria(models.Model): ...  ← extraer categoria a FK
    # class Emprendedor(models.Model): ...
    # class Inscripcion(models.Model): ...


    # --- BLOQUE 1: Configuración de Usuarios (Elías) ---
    # Aquí van  Emprendedor, Visitante, User (complejidad media-alta)


# Clase que nos permite manejar a los Emprendedores con los metodos que querramos
class EmprendedorManager(models.Manager):
    def listar_activos(self):
        return self.get_queryset().order_by('apellido', 'nombre')
    
    # Ejemplo de uso:
    # lista_emprendedores = Emprendedor.objects.listar_activos()

class Emprendedor(ValidableModel):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    rubro = models.ForeignKey(Feria, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = EmprendedorManager()

    def __str__(self):
        """Retorna una representación legible del nombre del emprendedor"""
        return self.nombre

    @classmethod
    def validate(cls, **kwargs) -> list[str]:
        """
        Valida los datos del Emprendedor. Retorna una lista de errores.
        Si la lista está vacía, los datos son válidos.
        """
        errors = []

        # Extracción segura para textos: saca espacios en blanco extra y evita que sea 'None'
        nombre = kwargs.get('nombre', '').strip() if kwargs.get('nombre') else ''
        apellido = kwargs.get('apellido', '').strip() if kwargs.get('apellido') else ''
        email = kwargs.get('email', '').strip() if kwargs.get('email') else ''
        telefono = kwargs.get('telefono', '').strip() if kwargs.get('telefono') else ''
        
        # Extracción segura para Objetos/IDs (Foreign Keys): no se les puede hacer .strip()
        rubro = kwargs.get('rubro')
        usuario = kwargs.get('usuario')

        # --- VALIDACIONES ---
        if not nombre:
            errors.append("El nombre es obligatorio.")

        if not apellido:
            errors.append("El apellido es obligatorio.")

        if not email:
            errors.append("El email es obligatorio.")

        if rubro is None:
            errors.append("El rubro es obligatorio.")

        if usuario is None:
            errors.append("El usuario es obligatorio.")

        return errors

class Visitante(ValidableModel):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_registro = models.DateField()

    def __str__(self):
        """Retorna una representación legible del nombre del visitante"""
        return self.nombre
    
    @classmethod
    def validate(cls, **kwargs) -> list[str]:
        """
        Valida los datos del visitante. Retorna una lista de errores.
        Si la lista está vacía, los datos son válidos.
        """
        errors = []

        # Extracción segura para textos: saca espacios en blanco extra y evita que sea 'None'
        nombre = kwargs.get('nombre', '').strip() if kwargs.get('nombre') else ''
        apellido = kwargs.get('apellido', '').strip() if kwargs.get('apellido') else ''
        email = kwargs.get('email', '').strip() if kwargs.get('email') else ''
        
        # Extracción segura para Objetos/IDs (Foreign Keys): no se les puede hacer .strip()
        fecha_registro = kwargs.get('fecha_registro')
        usuario = kwargs.get('usuario')

        # --- VALIDACIONES ---
        if not nombre:
            errors.append("El nombre es obligatorio.")

        if not apellido:
            errors.append("El apellido es obligatorio.")

        if not email:
            errors.append("El email es obligatorio.")

        if fecha_registro is None:
            errors.append("La fecha de registro es obligatoria.")

        if usuario is None:
            errors.append("El usuario es obligatorio.")

        return errors

    # --- BLOQUE 2: Estructura de Ferias (Persona B) ---
    # Aquí van Categoria, Feria, Sector (complejidad media)

    # --- BLOQUE 3: Transacciones (Persona C) ---
    # Aquí va Inscripcion (dependencia con Emprendedor, Feria y Sector) (complejidad alta)

    # --- BLOQUE 4: Feedback y Notificaciones (Persona D) ---
    # Aquí van Reseña(vincula Visistante con la Feria), Notificacion(cualquier User con alertas de sistema) (complejidad media)


# NOTA DE ELIAS PARA LA CLASE NOTIFICACIONES:
# Usen directamente como atributo dentro de la clase: usuarios = models.ManyToMany(User, related_name='notificaciones')
# Django lee esa línea y automáticamente viaja a la clase User original y le "inyecta" un atributo dinámico llamado exactamente como se indica en tu related_name.
# eso nos evita crear desde cero la clase User.