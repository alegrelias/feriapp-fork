"""Tests de comportamiento para el modelo Feria."""

from datetime import date

from django.test import TestCase

from django.contrib.auth.models import User

from app.models import Feria, Emprendedor, Visitante


class FeriaModelTest(TestCase):
    """Verifica validaciones y operaciones básicas del modelo Feria."""

    def setUp(self):
        """Crea una feria base reutilizable para cada caso de prueba."""
        self.feria = Feria.objects.create(
            nombre="Feria de Invierno",
            categoria="Artesanías",
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
            categoria="Tecnología",
            fecha_inicio=date(2026, 9, 1),
            fecha_fin=date(2026, 9, 3),
            ubicacion="Centro Cultural",
            capacidad_puestos=20,
        )
        self.assertEqual(errors, [])

    def test_validate_nombre_vacio_retorna_error(self):
        errors = Feria.validate(
            nombre="",
            categoria="Tecnología",
            fecha_inicio=date(2026, 9, 1),
            fecha_fin=date(2026, 9, 3),
            ubicacion="Centro Cultural",
            capacidad_puestos=20,
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_fecha_fin_anterior_a_inicio_retorna_error(self):
        errors = Feria.validate(
            nombre="Tech Patagonia",
            categoria="Tecnología",
            fecha_inicio=date(2026, 9, 10),
            fecha_fin=date(2026, 9, 5), # fin < inicio
            ubicacion="Centro Cultural",
            capacidad_puestos=20,
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_capacidad_cero_retorna_error(self):
        errors = Feria.validate(
            nombre="Tech Patagonia",
            categoria="Tecnología",
            fecha_inicio=date(2026, 9, 1),
            fecha_fin=date(2026, 9, 3),
            ubicacion="Centro Cultural",
            capacidad_puestos=0,
        )
        self.assertTrue(len(errors) > 0)

    # --- new ---

    def test_new_crea_feria_con_datos_validos(self):
        feria, errors = Feria.new(
            nombre="Mercado de Diseño",
            categoria="Artesanías",
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
            categoria="",
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
            categoria="Artesanías",
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
            categoria="",
            fecha_inicio=None,
            fecha_fin=None,
            ubicacion="",
            capacidad_puestos=0,
        )
        self.assertTrue(len(errors) > 0)
        self.feria.refresh_from_db()
        self.assertEqual(self.feria.nombre, "Feria de Invierno")  # sin cambios

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

        self.feria = Feria.objects.create(
            nombre="Feria de Invierno",
            categoria="Artesanías",
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