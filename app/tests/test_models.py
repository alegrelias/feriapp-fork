"""Tests de comportamiento para el modelo Feria."""

from datetime import date

from django.test import TestCase

from django.contrib.auth.models import User

from app.models import Categoria, Feria, Sector, Emprendedor, Visitante, Inscripcion


class CategoriaModelTest(TestCase):

    def test_validate_datos_correctos_retorna_lista_vacia(self):

        errors = Categoria.validate(
            nombre="Tecnologia",
            descripcion="Ferias tecnológicas"
        )

        self.assertEqual(errors, [])

    def test_validate_nombre_vacio_retorna_error(self):

        errors = Categoria.validate(
            nombre="",
            descripcion="Desc"
        )

        self.assertTrue(len(errors) > 0)

    def test_validate_nombre_corto_retorna_error(self):

        errors = Categoria.validate(
            nombre="AB",
            descripcion="Desc"
        )

        self.assertTrue(len(errors) > 0)

    def test_validate_descripcion_vacia_retorna_error(self):

        errors = Categoria.validate(
            nombre="Tecnologia",
            descripcion=""
        )

        self.assertTrue(len(errors) > 0)

    def test_new_crea_categoria(self):

        categoria, errors = Categoria.new(
            nombre="Gaming",
            descripcion="Eventos gaming"
        )

        self.assertEqual(errors, [])

        self.assertIsNotNone(categoria)

    def test_update_modifica_categoria(self):

        categoria = Categoria.objects.create(
            nombre="Old",
            descripcion="Desc"
        )

        errors = categoria.update(
            nombre="Nueva",
            descripcion="Nueva descripcion"
        )

        self.assertEqual(errors, [])

        categoria.refresh_from_db()

        self.assertEqual(
            categoria.nombre,
            "Nueva"
        )

class FeriaModelTest(TestCase):
    """Verifica validaciones y operaciones básicas del modelo Feria."""

    def setUp(self):
        """Crea una feria base reutilizable para cada caso de prueba."""
        self.categoria = Categoria.objects.create(
            nombre="Artesanías",
            descripcion="Ferias artesanales"
        )
        self.feria = Feria.objects.create(
            nombre="Feria de Invierno",
            categoria=self.categoria,
            fecha_inicio=date(2026, 7, 1),
            fecha_fin=date(2026, 7, 3),
            ubicacion="Plaza Central",
            capacidad_puestos=10,
        )

    # --- __str__ y métodos simples ---

    def test_str_retorna_nombre(self):
        self.assertEqual(str(self.feria), "Feria de Invierno")

    def test_activa_por_defecto(self):
        self.assertTrue(self.feria.activa)

    def test_puestos_disponibles_igual_a_capacidad_sin_inscripciones(self):
        self.assertEqual(self.feria.puestos_disponibles(), 10)

    def test_tiene_lugar_true_con_capacidad_libre(self):
        self.assertTrue(self.feria.tiene_lugar())

    # --- validate ---

    def test_validate_datos_correctos_retorna_lista_vacia(self):
        errors = Feria.validate(
            nombre="Tech Patagonia",
            categoria=self.categoria,
            fecha_inicio=date(2026, 9, 1),
            fecha_fin=date(2026, 9, 3),
            ubicacion="Centro Cultural",
            capacidad_puestos=20,
        )
        self.assertEqual(errors, [])

    def test_validate_nombre_vacio_retorna_error(self):
        errors = Feria.validate(
            nombre="",
            categoria=self.categoria,
            fecha_inicio=date(2026, 9, 1),
            fecha_fin=date(2026, 9, 3),
            ubicacion="Centro Cultural",
            capacidad_puestos=20,
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_fecha_fin_anterior_a_inicio_retorna_error(self):
        errors = Feria.validate(
            nombre="Tech Patagonia",
            categoria=self.categoria,
            fecha_inicio=date(2026, 9, 10),
            fecha_fin=date(2026, 9, 5), # fin < inicio
            ubicacion="Centro Cultural",
            capacidad_puestos=20,
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_capacidad_cero_retorna_error(self):
        errors = Feria.validate(
            nombre="Tech Patagonia",
            categoria=self.categoria,
            fecha_inicio=date(2026, 9, 1),
            fecha_fin=date(2026, 9, 3),
            ubicacion="Centro Cultural",
            capacidad_puestos=0,
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_categoria_none_retorna_error(self):

        errors = Feria.validate(
        nombre="Tech",
        categoria=None,
        fecha_inicio=date(2026, 9, 1),
        fecha_fin=date(2026, 9, 3),
        ubicacion="Centro",
        capacidad_puestos=10
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_ubicacion_vacia_retorna_error(self):

        errors = Feria.validate(
        nombre="Tech",
        categoria=self.categoria,
        fecha_inicio=date(2026, 9, 1),
        fecha_fin=date(2026, 9, 10),
        ubicacion="",
        capacidad_puestos=10
        )
        self.assertTrue(len(errors) > 0)

    # --- new ---

    def test_new_crea_feria_con_datos_validos(self):
        feria, errors = Feria.new(
            nombre="Mercado de Diseño",
            categoria=self.categoria,
            fecha_inicio=date(2026, 9, 1),
            fecha_fin=date(2026, 9, 3),
            ubicacion="Muelle Turístico",
            capacidad_puestos=20,
        )
        self.assertEqual(errors, [])
        self.assertIsNotNone(feria)
        self.assertEqual(feria.nombre, "Mercado de Diseño")
        self.assertTrue(Feria.objects.filter(nombre="Mercado de Diseño").exists())

    def test_new_con_datos_invalidos_retorna_errores_y_no_crea(self):
        count_antes = Feria.objects.count()
        feria, errors = Feria.new(
            nombre="",
            categoria=None,
            fecha_inicio=None,
            fecha_fin=None,
            ubicacion="",
            capacidad_puestos=0,
        )
        self.assertIsNone(feria)
        self.assertTrue(len(errors) > 0)
        self.assertEqual(Feria.objects.count(), count_antes)

    # --- update ---

    def test_update_modifica_datos_correctamente(self):
        errors = self.feria.update(
            nombre="Feria de Invierno",
            categoria=self.categoria,
            fecha_inicio=date(2026, 9, 1),
            fecha_fin=date(2026, 9, 3),
            ubicacion="Parque Central",
            capacidad_puestos=20,
        )
        self.assertEqual(errors, [])
        self.feria.refresh_from_db()
        self.assertEqual(self.feria.ubicacion, "Parque Central")
        self.assertEqual(self.feria.capacidad_puestos, 20)

    def test_update_con_datos_invalidos_no_modifica(self):
        errors = self.feria.update(
            nombre="",
            categoria=None,
            fecha_inicio=None,
            fecha_fin=None,
            ubicacion="",
            capacidad_puestos=0,
        )
        self.assertTrue(len(errors) > 0)
        self.feria.refresh_from_db()
        self.assertEqual(self.feria.nombre, "Feria de Invierno")  # sin cambios

class SectorModelTest(TestCase):

    def setUp(self):

        self.categoria = Categoria.objects.create(
            nombre="Tecnologia",
            descripcion="Desc"
        )

        self.feria = Feria.objects.create(
            nombre="Feria Tech",
            categoria=self.categoria,
            fecha_inicio=date(2026, 9, 1),
            fecha_fin=date(2026, 9, 10),
            ubicacion="Ushuaia",
            capacidad_puestos=20
        )

    def test_validate_datos_correctos(self):

        errors = Sector.validate(
            nombre="Sector A",
            feria=self.feria,
            edicion=1,
            capacidad_puestos=10
        )

        self.assertEqual(errors, [])

    def test_validate_nombre_vacio(self):

        errors = Sector.validate(
            nombre="",
            feria=self.feria,
            edicion=1,
            capacidad_puestos=10
        )

        self.assertTrue(len(errors) > 0)

    def test_validate_feria_none(self):

        errors = Sector.validate(
            nombre="Sector A",
            feria=None,
            edicion=1,
            capacidad_puestos=10
        )

        self.assertTrue(len(errors) > 0)

    def test_validate_edicion_invalida(self):

        errors = Sector.validate(
            nombre="Sector A",
            feria=self.feria,
            edicion=0,
            capacidad_puestos=10
        )

        self.assertTrue(len(errors) > 0)

    def test_validate_capacidad_invalida(self):

        errors = Sector.validate(
            nombre="Sector A",
            feria=self.feria,
            edicion=1,
            capacidad_puestos=0
        )

        self.assertTrue(len(errors) > 0)

    def test_new_crea_sector(self):

        sector, errors = Sector.new(
            feria=self.feria,
            edicion=1,
            nombre="Sector Norte",
            capacidad_puestos=15,
            tiene_conexion_electrica=True
        )

        self.assertEqual(errors, [])

        self.assertIsNotNone(sector)

    def test_update_modifica_sector(self):

        sector = Sector.objects.create(
            feria=self.feria,
            edicion=1,
            nombre="Sector A",
            capacidad_puestos=10
        )

        errors = sector.update(
            feria=self.feria,
            edicion=2,
            nombre="Sector B",
            capacidad_puestos=20,
            tiene_conexion_electrica=True
        )

        self.assertEqual(errors, [])

        sector.refresh_from_db()

        self.assertEqual(
            sector.nombre,
            "Sector B"
        )

    def test_hay_lugar(self):

        sector = Sector.objects.create(
            feria=self.feria,
            edicion=1,
            nombre="Sector A",
            capacidad_puestos=5
        )

        self.assertTrue(
            sector.hay_lugar()
        )

    # TODO: agregar tests para Inscripcion cuando lo implementen:
    # def test_tiene_lugar_false_cuando_llena(self): ...
    # def test_puestos_ocupados_cuenta_solo_confirmadas(self): ...


class EmprendedorModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="jhondoe",
            email="doejhon@gmail.com",
            password="password123"
        )

        self.categoria = Categoria.objects.create(
            nombre="Artesanías",
            descripcion="Ferias artesanales"
        )

        self.feria = Feria.objects.create(
            nombre="Feria de Invierno",
            categoria=self.categoria,
            fecha_inicio=date(2026, 7, 1),
            fecha_fin=date(2026, 7, 3),
            ubicacion="Plaza Central",
            capacidad_puestos=10,
        )

        self.emprendedor = Emprendedor.objects.create(
            nombre="Jhon",
            apellido="Doe",
            email="doejhon@gmail.com",
            rubro=self.feria,
            telefono="+54-2901 532133",
            usuario=self.user
        )

    def test_str_retorna_nombre(self):
        self.assertEqual(str(self.emprendedor), "Jhon")

    def test_listar_activos_ordenados(self):
        user2 = User.objects.create_user(
            username="patricio",
            email="estrella@gmail.com"
        )

        emprendedor_b = Emprendedor.objects.create(
            nombre="Patricio",
            apellido="Arenas",
            email="arenas@gmail.com",
            rubro=self.feria,
            telefono="+54-2901 999999",
            usuario=user2
        )

        lista_activos = Emprendedor.objects.listar_activos()
        self.assertEqual(lista_activos[0], emprendedor_b)
        self.assertEqual(lista_activos[1], self.emprendedor)


    # --- validate ---
    def test_validate_datos_correctos_retorna_lista_vacia(self):
        errors=Emprendedor.validate(
            nombre="Juan",
            apellido="Perez",
            email="jperez@gmail.com",
            rubro=self.feria,
            telefono="+54 2901 112233",
            usuario=self.user
        )
        #Debe devolver una lista vacia
        self.assertEqual(errors, [])

    def test_validate_error_falta_nombre(self):
        errors = Emprendedor.validate(
            nombre="",
            apellido="Perez",
            email="jperez@gmail.com",
            rubro=self.feria,
            telefono="+54 2901 112233",
            usuario=self.user
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_error_falta_feria(self):
        errors = Emprendedor.validate(
            nombre="Juan",
            apellido="Perez",
            email="jperez@gmail.com",
            rubro=None,
            telefono="+54 2901 112233",
            usuario=self.user
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_error_falta_user(self):
        errors = Emprendedor.validate(
            nombre="Juan",
            apellido="Perez",
            email="jperez@gmail.com",
            rubro=self.feria,
            telefono="+54 2901 112233",
            usuario=None
        )
        self.assertTrue(len(errors) > 0)

    # --- new ---
    def test_new_crea_emprendedor_con_datos_validos(self):
        emprendedor, errors = Emprendedor.new(
            nombre="Juan",
            apellido="Perez",
            email="jperez@gmail.com",
            rubro=self.feria,
            telefono="+54 2901 112233",
            usuario=self.user
        )
        self.assertEqual(errors, [])
        self.assertIsNotNone(emprendedor)
        self.assertEqual(emprendedor.nombre, "Juan")
        self.assertTrue(Emprendedor.objects.filter(nombre="Juan").exists())

    def test_new_con_datos_invalidos_retorna_errores_y_no_crea(self):
        count_antes = Emprendedor.objects.count()
        emprendedor, errors = Emprendedor.new(
            nombre="",
            apellido="",
            email="",
            rubro=None,
            telefono="",
            usuario=None)
        self.assertIsNone(emprendedor)
        self.assertTrue(len(errors) > 0)
        self.assertEqual(Emprendedor.objects.count(), count_antes)

    # --- update ---
    def test_update_modifica_datos_correctamente(self):
        errors = self.emprendedor.update(
            nombre="Juan",
            apellido="Perez",
            email="jperez@hotmail.com",
            rubro=self.feria,
            telefono="+54 2901 556677",
            usuario=self.user
        )
        self.assertEqual(errors, [])
        self.emprendedor.refresh_from_db()
        self.assertEqual(self.emprendedor.email, "jperez@hotmail.com")
        self.assertEqual(self.emprendedor.telefono, "+54 2901 556677")

    def test_update_con_datos_invalidos_no_modifica(self):
        errors = self.emprendedor.update(
            nombre="",
            apellido="",
            email="",
            rubro=None,
            telefono="",
            usuario=None)
        self.assertTrue(len(errors) > 0)
        self.emprendedor.refresh_from_db()
        self.assertEqual(self.emprendedor.nombre, "Jhon")  # sin cambios

class VisitanteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="jhondoe",
            email="doejhon@gmail.com",
            password="password123"
        )

        self.visitante = Visitante.objects.create(
            nombre="Jhon",
            apellido="Doe",
            email="doejhon@gmail.com",
            usuario=self.user,
            fecha_registro=date(2026, 7, 1),
        )

    def test_str_retorna_nombre(self):
        self.assertEqual(str(self.visitante), "Jhon")

    # --- validate ---
    def test_validate_datos_correctos_retorna_lista_vacia(self):
        errors=Visitante.validate(
            nombre="Juan",
            apellido="Perez",
            email="jperez@gmail.com",
            usuario=self.user,
            fecha_registro=date(2026, 9, 1)
        )
        #Debe devolver una lista vacia
        self.assertEqual(errors, [])

    def test_validate_error_falta_nombre(self):
        errors = Visitante.validate(
            nombre="",
            apellido="Perez",
            email="jperez@gmail.com",
            usuario=self.user,
            fecha_registro=date(2026, 9, 1)
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_error_falta_fecha(self):
        errors = Visitante.validate(
            nombre="Juan",
            apellido="Perez",
            email="jperez@gmail.com",
            usuario=self.user,
            fecha_registro=None
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_error_falta_user(self):
        errors = Visitante.validate(
            nombre="Juan",
            apellido="Perez",
            email="jperez@gmail.com",
            usuario=None,
            fecha_registro=date(2026, 1, 1)
        )
        self.assertTrue(len(errors) > 0)

    # --- new ---
    def test_new_crea_visitante_con_datos_validos(self):
        visitante, errors = Visitante.new(
            nombre="Juan",
            apellido="Perez",
            email="jperez@gmail.com",
            usuario=self.user,
            fecha_registro=date(2026, 9, 1)
        )
        self.assertEqual(errors, [])
        self.assertIsNotNone(visitante)
        self.assertEqual(visitante.nombre, "Juan")
        self.assertTrue(Visitante.objects.filter(nombre="Juan").exists())

    def test_new_con_datos_invalidos_retorna_errores_y_no_crea(self):
        count_antes = Visitante.objects.count()
        visitante, errors = Visitante.new(
            nombre="",
            apellido="",
            email="",
            usuario=None,
            fecha_registro=None)
        self.assertIsNone(visitante)
        self.assertTrue(len(errors) > 0)
        self.assertEqual(Visitante.objects.count(), count_antes)

    # --- update ---
    def test_update_modifica_datos_correctamente(self):
        errors = self.visitante.update(
            nombre="Juan",
            apellido="Perez",
            email="jperez@hotmail.com",
            usuario=self.user,
            fecha_registro=date(2026, 9, 3)
        )
        self.assertEqual(errors, [])
        self.visitante.refresh_from_db()
        self.assertEqual(self.visitante.email, "jperez@hotmail.com")
        self.assertEqual(self.visitante.fecha_registro, date(2026, 9, 3))

    def test_update_con_datos_invalidos_no_modifica(self):
        errors = self.visitante.update(
            nombre="",
            apellido="",
            email="",
            usuario=None,
            fecha_registro=None)
        self.assertTrue(len(errors) > 0)
        self.visitante.refresh_from_db()
        self.assertEqual(self.visitante.nombre, "Jhon")  # sin cambios

class InscripcionModelTest(TestCase):

    def setUp(self):
        """Crea datos base reutilizables"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@gmail.com"
        )

        self.categoria = Categoria.objects.create(
            nombre="Artesanías",
            descripcion="Ferias artesanales"
        )

        self.feria = Feria.objects.create(
            nombre="Feria de Invierno",
            categoria=self.categoria,
            fecha_inicio=date(2026, 7, 1),
            fecha_fin=date(2026, 7, 3),
            ubicacion="Plaza Central",
            capacidad_puestos=10
        )

        self.emprendedor = Emprendedor.objects.create(
            nombre="Juan",
            apellido="Perez",
            email="jperez@gmail.com",
            rubro=self.feria,
            telefono="+54-2901 112233",
            usuario=self.user
        )

    # --- __str__ ---

    def test_str_retorna_formato_correcto(self):
        inscripcion = Inscripcion.objects.create(
            emprendedor=self.emprendedor,
            feria=self.feria,
            registrado_por="admin"
        )
        self.assertEqual(str(inscripcion), f"Inscripción {inscripcion.id} - {self.emprendedor}")

    # --- validate ---

    def test_validate_datos_correctos_retorna_lista_vacia(self):
        errors = Inscripcion.validate(
            emprendedor=self.emprendedor,
            feria=self.feria,
            estado="Confirmada",
            numero_puesto=5,
            registrado_por="admin"
        )
        self.assertEqual(errors, [])

    def test_validate_error_falta_emprendedor(self):
        errors = Inscripcion.validate(
            emprendedor=None,
            feria=self.feria,
            registrado_por="admin"
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_error_falta_feria(self):
        errors = Inscripcion.validate(
            emprendedor=self.emprendedor,
            feria=None,
            registrado_por="admin"
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_error_falta_registrado_por(self):
        errors = Inscripcion.validate(
            emprendedor=self.emprendedor,
            feria=self.feria,
            registrado_por=""
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_error_puesto_negativo(self):
        errors = Inscripcion.validate(
            emprendedor=self.emprendedor,
            feria=self.feria,
            numero_puesto=-5,
            registrado_por="admin"
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_error_puesto_cero(self):
        errors = Inscripcion.validate(
            emprendedor=self.emprendedor,
            feria=self.feria,
            numero_puesto=0,
            registrado_por="admin"
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_error_confirmada_sin_puesto(self):
        errors = Inscripcion.validate(
            emprendedor=self.emprendedor,
            feria=self.feria,
            estado="Confirmada",
            numero_puesto=None,
            registrado_por="admin"
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_error_puesto_en_lista_espera(self):
        errors = Inscripcion.validate(
            emprendedor=self.emprendedor,
            feria=self.feria,
            estado="Lista_espera",
            numero_puesto=5,
            registrado_por="admin"
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_error_puesto_en_cancelada(self):
        errors = Inscripcion.validate(
            emprendedor=self.emprendedor,
            feria=self.feria,
            estado="Cancelada",
            numero_puesto=5,
            registrado_por="admin"
        )
        self.assertTrue(len(errors) > 0)

    # --- new ---

    def test_new_crea_inscripcion_con_datos_validos(self):
        inscripcion, errors = Inscripcion.new(
            emprendedor=self.emprendedor,
            feria=self.feria,
            estado="Confirmada",
            numero_puesto=3,
            registrado_por="admin"
        )
        self.assertEqual(errors, [])
        self.assertIsNotNone(inscripcion)
        self.assertEqual(inscripcion.emprendedor, self.emprendedor)
        self.assertEqual(inscripcion.numero_puesto, 3)

    def test_new_estado_por_defecto_lista_espera(self):
        inscripcion, errors = Inscripcion.new(
            emprendedor=self.emprendedor,
            feria=self.feria,
            registrado_por="admin"
        )
        self.assertEqual(errors, [])
        self.assertEqual(inscripcion.estado, "Lista_espera")

    def test_new_con_datos_invalidos_retorna_errores_y_no_crea(self):
        count_antes = Inscripcion.objects.count()
        inscripcion, errors = Inscripcion.new(
            emprendedor=None,
            feria=None,
            registrado_por=""
        )
        self.assertIsNone(inscripcion)
        self.assertTrue(len(errors) > 0)
        self.assertEqual(Inscripcion.objects.count(), count_antes)

    # --- update ---

    def test_update_puesto_en_inscripcion_confirmada_falla_por_bug_de_estado_none(self):
        """
        Demuestra el bug crítico: Al actualizar SOLO el número de puesto
        en una inscripción que ya está Confirmada, el sistema falla
        porque 'estado' no viaja en los kwargs y validate asume que es None.
        """
        # 1. Creamos una inscripción que nace correctamente Confirmada y con puesto
        inscripcion_confirmada = Inscripcion.objects.create(
            emprendedor=self.emprendedor,
            feria=self.feria,
            estado="Confirmada",
            numero_puesto=5,
            registrado_por="admin_test"
        )

        # 2. Intentamos cambiar SOLAMENTE el número de puesto (del 5 al 10)
        # Pasamos los datos tal como lo configuraste en tu código
        errors = inscripcion_confirmada.update(numero_puesto=10)

        # 3. VERIFICACIÓN DEL COMPORTAMIENTO:
        # El test va a fallar acá en tu código actual porque la lista de errores NO va a estar vacía.
        # Va a contener el error: "No se puede asignar un número de puesto si la inscripción no está en estado 'Confirmada'."
        self.assertEqual(errors, [], f"El update falló con los siguientes errores: {errors}")

        # 4. Verificación de persistencia en la base de datos
        inscripcion_confirmada.refresh_from_db()
        self.assertEqual(inscripcion_confirmada.numero_puesto, 10)

    def test_update_mismo_puesto_en_otra_inscripcion_falla(self):
        """
        Caso A: Valida que el sistema PROHÍBA asignar un puesto
        que ya está ocupado por otra inscripción confirmada.
        """
        # 1. Creamos la primera inscripción confirmada en el puesto 5
        Inscripcion.objects.create(
            emprendedor=self.emprendedor,
            feria=self.feria,
            estado="Confirmada",
            numero_puesto=5,
            registrado_por="admin"
        )

        # 2. Creamos una segunda inscripción en lista de espera
        inscripcion_2 = Inscripcion.objects.create(
            emprendedor=self.emprendedor,
            feria=self.feria,
            estado="Lista_espera",
            registrado_por="admin"
        )

        # 3. Intentamos actualizar la segunda inscripción al mismo puesto 5
        errors = inscripcion_2.update(estado="Confirmada", numero_puesto=5)

        # 4. Verificación: La lista de errores NO debe estar vacía
        self.assertTrue(len(errors) > 0, "El sistema debió rechazar el puesto duplicado")
        self.assertIn("ya se encuentra ocupado en esta feria", errors[0])

    def test_update_modifica_datos_correctamente(self):
        inscripcion = Inscripcion.objects.create(
            emprendedor=self.emprendedor,
            feria=self.feria,
            registrado_por="admin"
        )

        errors = inscripcion.update(
            estado="Confirmada",
            numero_puesto=7
        )

        self.assertEqual(errors, [])
        inscripcion.refresh_from_db()
        self.assertEqual(inscripcion.estado, "Confirmada")
        self.assertEqual(inscripcion.numero_puesto, 7)

    def test_update_error_cambiar_emprendedor(self):
        user2 = User.objects.create_user(username="otro", email="otro@gmail.com")
        emprendedor2 = Emprendedor.objects.create(
            nombre="Pedro",
            apellido="Lopez",
            email="plopez@gmail.com",
            rubro=self.feria,
            telefono="+54-2901 999999",
            usuario=user2
        )

        inscripcion = Inscripcion.objects.create(
            emprendedor=self.emprendedor,
            feria=self.feria,
            registrado_por="admin"
        )

        errors = inscripcion.update(emprendedor=emprendedor2)
        self.assertTrue(len(errors) > 0)

    def test_update_error_cambiar_feria(self):
        feria2 = Feria.objects.create(
            nombre="Otra Feria",
            categoria=self.categoria,
            fecha_inicio=date(2026, 8, 1),
            fecha_fin=date(2026, 8, 3),
            ubicacion="Otro Lugar",
            capacidad_puestos=5
        )

        inscripcion = Inscripcion.objects.create(
            emprendedor=self.emprendedor,
            feria=self.feria,
            registrado_por="admin"
        )

        errors = inscripcion.update(feria=feria2)
        self.assertTrue(len(errors) > 0)

    def test_update_error_cambiar_registrado_por(self):
        inscripcion = Inscripcion.objects.create(
            emprendedor=self.emprendedor,
            feria=self.feria,
            registrado_por="admin"
        )

        errors = inscripcion.update(registrado_por="otro_admin")
        self.assertTrue(len(errors) > 0)

    def test_update_error_confirmar_desde_cancelada(self):
        inscripcion = Inscripcion.objects.create(
            emprendedor=self.emprendedor,
            feria=self.feria,
            estado="Cancelada",
            registrado_por="admin"
        )

        errors = inscripcion.update(estado="Confirmada", numero_puesto=5)
        self.assertTrue(len(errors) > 0)

    def test_update_error_volver_a_lista_espera(self):
        inscripcion = Inscripcion.objects.create(
            emprendedor=self.emprendedor,
            feria=self.feria,
            estado="Confirmada",
            numero_puesto=5,
            registrado_por="admin"
        )

        errors = inscripcion.update(estado="Lista_espera")
        self.assertTrue(len(errors) > 0)

    def test_update_con_datos_invalidos_no_modifica(self):
        inscripcion = Inscripcion.objects.create(
            emprendedor=self.emprendedor,
            feria=self.feria,
            registrado_por="admin"
        )

        errors = inscripcion.update(estado="Confirmada", numero_puesto=0)
        self.assertTrue(len(errors) > 0)
        inscripcion.refresh_from_db()
        self.assertEqual(inscripcion.estado, "Lista_espera")

    # --- cancelar_inscripcion ---

    def test_cancelar_inscripcion_cambia_estado(self):
        inscripcion = Inscripcion.objects.create(
            emprendedor=self.emprendedor,
            feria=self.feria,
            registrado_por="admin"
        )

        inscripcion.cancelar_inscripcion()
        inscripcion.refresh_from_db()
        self.assertEqual(inscripcion.estado, "Cancelada")

    # --- listar_activos (Manager) ---

    def test_listar_activos_solo_retorna_confirmadas(self):
        Inscripcion.objects.create(
            emprendedor=self.emprendedor,
            feria=self.feria,
            estado="Confirmada",
            numero_puesto=1,
            registrado_por="admin"
        )

        Inscripcion.objects.create(
            emprendedor=self.emprendedor,
            feria=self.feria,
            estado="Lista_espera",
            registrado_por="admin"
        )

        activos = Inscripcion.objects.listar_activos()
        self.assertEqual(activos.count(), 1)
        self.assertEqual(activos[0].estado, "Confirmada")

class ReseniaModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="visitante1",
            email="visitante1@gmail.com",
            password="password123"
        )

    self.visitante = Visitante.objects.create(
        nombre="Harry",
        apellido="Potter",
        email="harrypotter1@gmail.com",
        usuario=self.user,
        fecha_registro=date(2026, 7, 1),
    )

    self.categoria = Categoria.objects.create(
        nombre="Tecnologia",
        descripcion="Ferias tecnológicas"
    )

    self.feria = Feria.objects.create(
        nombre="Feria Tech",
        categoria=self.categoria,
        fecha_inicio=date(2026, 9, 1),
        fecha_fin=date(2026, 9, 10),
        ubicacion="Ushuaia",
        capacidad_puestos=20
    )

    def test_str_retorna_formato_correcto(self):
        resenia = Resenia.objects.create(
            visitante=self.visitante,
            feria=self.feria,
            calificacion=4,
            comentario="Muy buena feria, la pasé genial!"
        )
        expected_str = f" Reseña de {self.visitante} para {self.feria.nombre} - Calificación: {resenia.calificacion}"
        self.assertEqual(str(resenia), expected_str)

    def test_validate_datos_correctos_retorna_lista_vacia(self):
        errors = Resenia.validate(
            visitante=self.visitante,
            feria=self.feria,
            calificacion=5,
            comentario="Excelente evento!"
        )
        self.assertEqual(errors, [])

    def test_validate_error_falta_visitante(self):
        errors = Resenia.validate(
            visitante=None,
            feria=self.feria,
            calificacion=5,
            comentario="Excelente evento!"
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_error_falta_feria(self):
        errors = Resenia.validate(
            visitante=self.visitante,
            feria=None,
            calificacion=5,
            comentario="Excelente evento!"
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_error_calificacion_fuera_de_rango(self):
        errors = Resenia.validate(
            visitante=self.visitante,
            feria=self.feria,
            calificacion=6,  # fuera de rango
            comentario="Excelente evento!"
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_error_calificacion_negativa(self):
        errors = Resenia.validate(
            visitante=self.visitante,
            feria=self.feria,
            calificacion=-1,  # fuera de rango
            comentario="No me gustó"
        )
        self.assertTrue(len(errors) > 0)

    def test_new_crea_resenia_con_datos_validos(self):
        resenia, errors = Resenia.new(
            visitante=self.visitante,
            feria=self.feria,
            calificacion=4,
            comentario="Muy buena feria!"
        )
        self.assertEqual(errors, [])
        self.assertIsNotNone(resenia)
        self.assertEqual(resenia.calificacion, 4)
        self.assertTrue(Resenia.objects.filter(id=resenia.id).exists())

    def test_new_con_datos_invalidos_retorna_errores_y_no_crea(self):
        count_antes = Resenia.objects.count()
        resenia, errors = Resenia.new(
            visitante=None,
            feria=None,
            calificacion=10,  # fuera de rango
            comentario=""
        )
        self.assertIsNone(resenia)
        self.assertTrue(len(errors) > 0)
        self.assertEqual(Resenia.objects.count(), count_antes)

    def test_update_modifica_datos_correctamente(self):
        resenia = Resenia.objects.create(
            visitante=self.visitante,
            feria=self.feria,
            calificacion=3,
            comentario="Estuvo bien"
        )

        errors = resenia.update(
            calificacion=5,
            comentario="¡Excelente evento!"
        )

        self.assertEqual(errors, [])
        resenia.refresh_from_db()
        self.assertEqual(resenia.calificacion, 5)
        self.assertEqual(resenia.comentario, "¡Excelente evento!")
