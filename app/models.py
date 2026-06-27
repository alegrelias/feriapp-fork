"""Modelos de dominio para la aplicación de ferias."""

from __future__ import annotations
from datetime import date


from django.db import models
from app.base_models import ValidableModel
#Importo esta clase que permite usar la clase "User" provista por Django
from django.contrib.auth.models import User

class Categoria(ValidableModel):
    """Representa una categoría de feria."""

    nombre = models.CharField(max_length=100,unique=True)
    descripcion = models.TextField()

    class Meta:
        ordering = ["nombre"]

    def __str__(self):

        return self.nombre

    def cantidad_ferias(self):
        """Retorna la cantidad de ferias asociadas."""

        return self.ferias.count()

    @classmethod
    def validate(cls, **kwargs) -> list[str]:

        errors = []

        nombre = (kwargs.get("nombre", "").strip() if kwargs.get("nombre") else "")
        descripcion = (kwargs.get("descripcion", "").strip() if kwargs.get("descripcion") else "")

        if not nombre:
            errors.append("El nombre es obligatorio.")

        if len(nombre) < 3:
            errors.append("El nombre debe tener al menos 3 caracteres.")

        if not descripcion:
            errors.append("La descripción es obligatoria.")

        return errors

class Feria(ValidableModel):#<- ya no heredamos de models.Models sino de ValidableModel
    """Representa una feria con su período, ubicación y capacidad disponible."""

    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="ferias", null=True, blank=True)
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

        return self.inscripciones_feria.filter(estado="Confirmada").count()

    def puestos_disponibles(self):
        """Retorna los puestos libres."""

        return (self.capacidad_puestos - self.puestos_ocupados())

    def tiene_lugar(self):
        """Retorna True si quedan puestos disponibles."""

        return self.puestos_disponibles() > 0

    def cantidad_sectores(self):
        """Retorna la cantidad de sectores asociados."""

        return self.sectores.count()
    
    def en_curso(self):
        hoy = date.today() 

        return  hoy >= self.fecha_inicio and hoy <= self.fecha_fin  
    
    def a_comenzar(self):
        hoy = date.today() 

        return  hoy < self.fecha_inicio
    
    def finalizada(self):
        hoy = date.today() 

        return  hoy > self.fecha_fin

    @classmethod
    def validate(cls, **kwargs) -> list[str]:
        """Valida los datos de la feria. Retorna una lista de errores."""

        errors = []

        nombre = (kwargs.get("nombre", "").strip() if kwargs.get("nombre") else "")
        ubicacion = (kwargs.get("ubicacion", "").strip() if kwargs.get("ubicacion") else "")
        categoria = kwargs.get("categoria")
        capacidad_puestos = kwargs.get("capacidad_puestos")
        fecha_inicio = kwargs.get("fecha_inicio")
        fecha_fin = kwargs.get("fecha_fin")

        if not nombre:
            errors.append("El nombre es obligatorio.")

        if categoria is None:
            errors.append("La categoría es obligatoria.")

        if not ubicacion:
            errors.append("La ubicación es obligatoria.")

        if (capacidad_puestos is None or capacidad_puestos <= 0):
            errors.append("La capacidad de puestos debe ser mayor a cero.")

        if (fecha_inicio and fecha_fin and fecha_fin < fecha_inicio):
            errors.append("La fecha de fin no puede ser anterior a la fecha de inicio.")

        return errors

class Sector(ValidableModel):
    """Representa un sector dentro de una feria."""

    feria = models.ForeignKey(Feria, on_delete=models.CASCADE, related_name="sectores")
    edicion = models.PositiveIntegerField()
    nombre = models.CharField(max_length=100)
    capacidad_puestos = models.PositiveIntegerField()
    tiene_conexion_electrica = models.BooleanField(default=False)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):

        return (
            f"{self.nombre} - "
            f"{self.feria.nombre}"
        )

    def hay_lugar(self):
        """Retorna True si el sector posee capacidad."""

        return self.capacidad_puestos > 0

    @classmethod
    def validate(cls, **kwargs) -> list[str]:

        errors = []

        nombre = (kwargs.get("nombre", "").strip() if kwargs.get("nombre") else "")
        feria = kwargs.get("feria")
        edicion = kwargs.get("edicion")
        capacidad_puestos = kwargs.get("capacidad_puestos")

        if not nombre:
            errors.append("El nombre es obligatorio.")

        if len(nombre) < 2:
            errors.append("El nombre debe tener al menos 2 caracteres.")

        if feria is None:
            errors.append("La feria es obligatoria.")

        if (edicion is None or edicion <= 0):
            errors.append("La edición debe ser mayor a cero.")

        if (capacidad_puestos is None or capacidad_puestos <= 0):
            errors.append("La capacidad debe ser mayor a cero.")

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
    def listar_ordenados(self):
        return self.get_queryset().order_by('apellido', 'nombre')

    # Ejemplo de uso:
    # lista_emprendedores = Emprendedor.objects.listar_ordenados()

class Emprendedor(ValidableModel):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    rubro = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
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

    # --- BLOQUE 3: Transacciones (Aby) ---
    # Aquí va Inscripcion (dependencia con Emprendedor, Feria y Sector) (complejidad alta)

    #  El Manager solo se encarga de las consultas de conjuntos (QuerySets), maneja la TABLA, las de objetos van como metodo de instancia
class InscripcionManager(models.Manager):
    #get_queryset() no lo sobrescribo, por ende hereda el de Django que trae TODO.

    def listar_activos(self):
        #'emprendedor__apellido' iajá a la tabla relacionada mediante la clave foránea emprendedor y ordená usando la columna apellido de esa otra tabla
        return self.get_queryset().filter(estado='Confirmada').order_by('emprendedor__apellido', 'emprendedor__nombre')



class Inscripcion(ValidableModel):

        emprendedor = models.ForeignKey(Emprendedor, on_delete= models.CASCADE, related_name='inscripciones_emprendedor')
        #que pasa si feria se borra?, null y blank quedan por defecto en false si no se colocan
        feria = models.ForeignKey(Feria, on_delete= models.CASCADE, related_name='inscripciones_feria')
        numero_puesto = models.IntegerField(null=True, blank=True)
        #se le asigna la fecha cuando fue guardada en el servidor, no se puede modificar
        fecha_inscripcion= models.DateField(auto_now_add=True)
        #debe ser lista de tuplas en choices
        ESTADOS_CHOICES = [
        ('Confirmada', 'Confirmada'),
        ('Lista_espera', 'Lista_espera'),
        ('Cancelada', 'Cancelada'),
    ]
        estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES , default='Lista_espera')
        registrado_por = models.CharField(max_length=100)

        #vinculo el manager
        
        class Meta:
            #para el panel de admin
            verbose_name_plural = "Inscripciones"
            ordering = ["fecha_inscripcion"]

        def __str__(self):
            #django detecta que quiero acceder al objeto completo de emprendedor, no solo el numero asi que hace join de las tablas y me trae el nombre
            return f"Inscripción {self.id} - {self.emprendedor}"

        def cancelar_inscripcion(self):

            self.estado = 'Cancelada'
            self.save()

        @classmethod
        def existe_puesto(cls, feria, numero_puesto, instancia_id=None) -> bool:
            """
            Consulta la BD para ver si el puesto ya está ocupado
            en esa feria específica por otra inscripción confirmada.
            """
            if not feria or not numero_puesto:
                return False

            puesto_ocupado = cls.objects.filter(
                feria=feria,
                numero_puesto=numero_puesto,
                estado='Confirmada'
            )

            # Si es update, excluimos el ID de la inscripción actual
            if instancia_id is not None:
                puesto_ocupado = puesto_ocupado.exclude(id=instancia_id)

            return puesto_ocupado.exists()


        @classmethod
        def validate(cls, **kwargs) -> list[str]:
        # si se llegara a agregar alguna validacion en la clase madre la ejecuta
            errors = super().validate(**kwargs)

            #si no hay parametro emprendedor, devuelvo un None
            emprendedor = kwargs.get("emprendedor",None)
            #si es texto le saco los espacios
            if isinstance(emprendedor,str):
                emprendedor= emprendedor.strip()
            #si hay cadena vacia o None entra al error
            if not emprendedor :
                errors.append("Es obligatorio indicar el emprendedor que solicita la inscripcion")

            feria = kwargs.get("feria",None)
            if isinstance(feria,str):
                feria= feria.strip()
                #si hay cadena vacia o None entra al error
            if not feria :
                errors.append("Es obligatorio indicar en que feria se solicita la inscripcion")

            numero_puesto = kwargs.get("numero_puesto", None)
            estado_enviado = kwargs.get("estado", None)
            estado_efectivo = estado_enviado or "Lista_espera"
            instancia_id = kwargs.get("instancia_id", None)

            if numero_puesto is not None:
                # Validar que sea un número válido
                if int(numero_puesto) <= 0:
                    errors.append("El número de puesto debe ser un entero positivo.")

                # Validar consistencia con el estado
                if estado_enviado is None:
                    # Caso A: El usuario no especificó estado pero metió un número de puesto
                    errors.append("No se puede asignar un número de puesto si la inscripción no está en estado 'Confirmada'.")
                elif estado_efectivo in ["Lista_espera", "Cancelada"]:
                    # Caso B: El usuario explícitamente eligió un estado inválido para tener puesto
                    errors.append(f"No se puede asignar un número de puesto a una inscripción con estado '{estado_efectivo}'.")

            if estado_efectivo == "Confirmada" and not numero_puesto:
                errors.append("Las inscripciones aceptadas deben tener un número de puesto asignado.")
            # --- VALIDACIÓN DE PUESTO DUPLICADO ---
            if estado_efectivo == "Confirmada":
                if cls.existe_puesto(feria, numero_puesto, instancia_id):
                    errors.append(f"El número de puesto {numero_puesto} ya se encuentra ocupado en esta feria.")

            registrado_por = kwargs.get("registrado_por", "")
            if isinstance(registrado_por, str):
                registrado_por = registrado_por.strip()

            if not registrado_por:
                errors.append("Debe especificarse el usuario que registra esta inscripción.")


            return errors

        def update(self, **kwargs) -> list[str]:
            """Sobreescribo el metodo porque igual hay que tener en cuenta casos propios de la instancia del modelo"""
            errors = []




            if "emprendedor" in kwargs and self.emprendedor != kwargs["emprendedor"]:
                errors.append("No se puede modificar el emprendedor de una inscripción existente. Debe cancelar la inscripcion")

            if "feria" in kwargs and self.feria != kwargs["feria"]:
                errors.append("No se puede modificar la feria de una inscripción existente. Debe cancelar la inscripcion")

            if "registrado_por" in kwargs and self.registrado_por != kwargs["registrado_por"].strip():
                errors.append("No se puede modificar el usuario que registró la inscripción.")


            nuevo_estado = kwargs.get("estado", None)
            if nuevo_estado and self.estado != nuevo_estado:
                if nuevo_estado == "Confirmada" and self.estado != "Lista_espera":
                    errors.append(f"No se puede confirmar una inscripción cuyo estado actual es '{self.estado}'. Debe estar en 'Lista_espera'.")

                if nuevo_estado == "Cancelada" and self.estado not in ["Lista_espera", "Confirmada"]:
                    errors.append(f"No se puede cancelar una inscripción cuyo estado actual es '{self.estado}'.")

                if nuevo_estado == "Lista_espera":
                    errors.append("No se puede cambiar el estado de una inscripción de regreso a 'Lista_espera'.")


            if errors:
                return errors

            #como validate si o si chequea que esten ciertos argumentos se los seteo como si hubieran sido enviado en el update
            kwargs.setdefault("feria", self.feria)
            kwargs.setdefault("emprendedor", self.emprendedor)
            kwargs.setdefault("registrado_por", self.registrado_por)
            kwargs.setdefault("estado", self.estado)
            kwargs['instancia_id'] = self.id

            return super().update(**kwargs)


    # --- BLOQUE 4: Feedback y Notificaciones (Persona D) ---
    # Aquí van Reseña(vincula Visistante con la Feria), Notificacion(cualquier User con alertas de sistema) (complejidad media)
class Resenia(ValidableModel):

    visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE, related_name='resenias')
    feria = models.ForeignKey(Feria, on_delete=models.CASCADE, related_name='resenias')
    calificacion = models.PositiveIntegerField()
    comentario = models.TextField(blank=True, null=True)
    fecha_resenia = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_resenia']

    def __str__(self):
        """Retorna una representación legible de la reseña"""
        return f"Reseña de {self.visitante.nombre} para {self.feria.nombre} ({self.calificacion}*)"

    @classmethod
    def validate(cls, **kwargs) -> list[str]:
        """
        Valida los datos de la reseña. Retorna una lista de errores.
        Si la lista está vacía, los datos son válidos.
        """
        errors = []

        # Extracción segura para textos: saca espacios en blanco extra y evita que sea 'None'
        comentario = kwargs.get('comentario', '').strip() if kwargs.get('comentario') else ''

        # Extracción segura para Objetos/IDs (Foreign Keys): no se les puede hacer .strip()
        visitante = kwargs.get('visitante')
        feria = kwargs.get('feria')
        calificacion = kwargs.get('calificacion')

        # --- VALIDACIONES ---
        if visitante is None:
            errors.append("El visitante es obligatorio.")

        if feria is None:
            errors.append("La feria es obligatoria.")

        if calificacion is None or not (1 <= calificacion <= 5):
            errors.append("La calificación debe ser un número entre 1 y 5.")

        return errors




# NOTA DE ELIAS PARA LA CLASE NOTIFICACIONES:
# Usen directamente como atributo dentro de la clase: usuarios = models.ManyToMany(User, related_name='notificaciones')
# Django lee esa línea y automáticamente viaja a la clase User original y le "inyecta" un atributo dinámico llamado exactamente como se indica en tu related_name.
# eso nos evita crear desde cero la clase User.

# NOTA DE DANIELA PARA LA CLASE RESENIA:
# unique_together = ('visitante', 'feria') // deberia ir esto para asegurar que no haya dos reseñas del mismo visitante para la misma feria?, pero lo dejo comentado por ahora para no complicar el desarrollo inicial.