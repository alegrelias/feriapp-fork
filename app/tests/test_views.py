# app/tests/test_views.py
"""Tests de comportamiento para las vistas de la aplicación de ferias."""

from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from app.models import Categoria, Feria, Emprendedor, Visitante, Inscripcion, Resenia


class HomeViewTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Tecnologia", descripcion="Desc")
        Feria.objects.create(
            nombre="Feria Tech", categoria=self.categoria,
            fecha_inicio=date.today() + timedelta(days=5),
            fecha_fin=date.today() + timedelta(days=7),
            ubicacion="Ushuaia", capacidad_puestos=10,
        )

    def test_home_status_200(self):
        response = self.client.get(reverse('ferias:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_usa_template_correcto(self):
        response = self.client.get(reverse('ferias:home'))
        self.assertTemplateUsed(response, 'ferias/home.html')

    def test_home_contiene_ferias_activas_en_contexto(self):
        response = self.client.get(reverse('ferias:home'))
        self.assertIn('ferias_activas', response.context)


class PerfilViewTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Gastronomia", descripcion="Desc")

        self.user_emp = User.objects.create_user(username="emp1", password="test1234")
        self.emprendedor = Emprendedor.objects.create(
            nombre="Juan", apellido="Perez", email="juan@test.com",
            rubro=self.categoria, telefono="123", usuario=self.user_emp,
        )

        self.user_vis = User.objects.create_user(username="vis1", password="test1234")
        self.visitante = Visitante.objects.create(
            nombre="Ana", apellido="Gomez", email="ana@test.com",
            usuario=self.user_vis, fecha_registro=date.today(),
        )

    def test_perfil_requiere_login(self):
        response = self.client.get(reverse('ferias:perfil'))
        self.assertEqual(response.status_code, 302)  # redirige a login

    def test_perfil_emprendedor_muestra_tipo_correcto(self):
        self.client.login(username="emp1", password="test1234")
        response = self.client.get(reverse('ferias:perfil'))
        self.assertEqual(response.context['tipo'], "Emprendedor")
        self.assertEqual(response.context['perfil'], self.emprendedor)

    def test_perfil_visitante_muestra_tipo_correcto(self):
        self.client.login(username="vis1", password="test1234")
        response = self.client.get(reverse('ferias:perfil'))
        self.assertEqual(response.context['tipo'], "Visitante")
        self.assertEqual(response.context['perfil'], self.visitante)

    def test_perfil_emprendedor_total_inscripciones(self):
        feria = Feria.objects.create(
            nombre="Feria 1", categoria=self.categoria,
            fecha_inicio=date.today() + timedelta(days=5),
            fecha_fin=date.today() + timedelta(days=7),
            ubicacion="Plaza", capacidad_puestos=10,
        )
        Inscripcion.objects.create(
            emprendedor=self.emprendedor, feria=feria,
            estado="Confirmada", numero_puesto=1, registrado_por="admin",
        )
        self.client.login(username="emp1", password="test1234")
        response = self.client.get(reverse('ferias:perfil'))
        self.assertEqual(response.context['total_inscripciones'], 1)
        self.assertEqual(response.context['total_confirmadas'], 1)


class FeriasListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="test1234")
        self.categoria = Categoria.objects.create(nombre="Tecnologia", descripcion="Desc")
        Feria.objects.create(
            nombre="Feria Activa", categoria=self.categoria,
            fecha_inicio=date.today() + timedelta(days=5),
            fecha_fin=date.today() + timedelta(days=7),
            ubicacion="Ushuaia", capacidad_puestos=10, activa=True,
        )
        Feria.objects.create(
            nombre="Feria Inactiva", categoria=self.categoria,
            fecha_inicio=date.today() + timedelta(days=5),
            fecha_fin=date.today() + timedelta(days=7),
            ubicacion="Ushuaia", capacidad_puestos=10, activa=False,
        )

    def test_requiere_login(self):
        response = self.client.get(reverse('ferias:lista_ferias'))
        self.assertEqual(response.status_code, 302)

    def test_lista_solo_ferias_activas(self):
        self.client.login(username="user1", password="test1234")
        response = self.client.get(reverse('ferias:lista_ferias'))
        nombres = [f.nombre for f in response.context['ferias']]
        self.assertIn("Feria Activa", nombres)
        self.assertNotIn("Feria Inactiva", nombres)

    def test_filtro_por_categoria(self):
        otra_categoria = Categoria.objects.create(nombre="Arte", descripcion="Desc")
        Feria.objects.create(
            nombre="Feria Arte", categoria=otra_categoria,
            fecha_inicio=date.today() + timedelta(days=5),
            fecha_fin=date.today() + timedelta(days=7),
            ubicacion="Centro", capacidad_puestos=5, activa=True,
        )
        self.client.login(username="user1", password="test1234")
        response = self.client.get(reverse('ferias:lista_ferias'), {'categoria': otra_categoria.id})
        nombres = [f.nombre for f in response.context['ferias']]
        self.assertEqual(nombres, ["Feria Arte"])


class NuevaFeriaViewTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Tecnologia", descripcion="Desc")

        self.user_sin_permiso = User.objects.create_user(username="user1", password="test1234")

        self.user_con_permiso = User.objects.create_user(username="admin1", password="test1234")
        permiso = Permission.objects.get(
            codename="add_feria",
            content_type=ContentType.objects.get_for_model(Feria),
        )
        self.user_con_permiso.user_permissions.add(permiso)

    def test_requiere_login(self):
        response = self.client.get(reverse('ferias:nueva_feria'))
        self.assertEqual(response.status_code, 302)

    def test_usuario_sin_permiso_no_puede_acceder(self):
        self.client.login(username="user1", password="test1234")
        response = self.client.get(reverse('ferias:nueva_feria'))
        self.assertEqual(response.status_code, 403)

    def test_usuario_con_permiso_puede_crear_feria(self):
        self.client.login(username="admin1", password="test1234")
        response = self.client.post(reverse('ferias:nueva_feria'), {
            'nombre': 'Feria Nueva',
            'categoria': self.categoria.id,
            'fecha_inicio': date.today() + timedelta(days=10),
            'fecha_fin': date.today() + timedelta(days=12),
            'ubicacion': 'Plaza Central',
            'capacidad_puestos': 15,
            'activa': True,
        })
        self.assertTrue(Feria.objects.filter(nombre='Feria Nueva').exists())
        self.assertRedirects(response, reverse('ferias:lista_ferias'))


class RegistroEmprendedorViewTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Tecnologia", descripcion="Desc")

    def test_registro_crea_user_y_emprendedor(self):
        response = self.client.post(reverse('ferias:registro_emprendedor'), {
            'username': 'nuevoemp',
            'password1': 'ContraseñaSegura123',
            'password2': 'ContraseñaSegura123',
            'nombre': 'Carlos',
            'apellido': 'Ruiz',
            'email': 'carlos@test.com',
            'telefono': '12345',
            'rubro': self.categoria.id,
        })
        self.assertTrue(User.objects.filter(username='nuevoemp').exists())
        self.assertTrue(Emprendedor.objects.filter(email='carlos@test.com').exists())
        self.assertRedirects(response, reverse('ferias:login'))

    def test_registro_datos_invalidos_no_crea_nada(self):
        count_antes = User.objects.count()
        response = self.client.post(reverse('ferias:registro_emprendedor'), {
            'username': '',
            'password1': '123',
            'password2': '456',  # no coincide
        })
        self.assertEqual(User.objects.count(), count_antes)
        self.assertEqual(response.status_code, 200)  # vuelve a mostrar el form con errores


class NuevaInscripcionViewTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Tecnologia", descripcion="Desc")
        self.feria = Feria.objects.create(
            nombre="Feria Tech", categoria=self.categoria,
            fecha_inicio=date.today() + timedelta(days=5),
            fecha_fin=date.today() + timedelta(days=7),
            ubicacion="Ushuaia", capacidad_puestos=10,
        )

        self.user_emp = User.objects.create_user(username="emp1", password="test1234")
        self.emprendedor = Emprendedor.objects.create(
            nombre="Juan", apellido="Perez", email="juan@test.com",
            rubro=self.categoria, telefono="123", usuario=self.user_emp,
        )

        self.user_vis = User.objects.create_user(username="vis1", password="test1234")
        Visitante.objects.create(
            nombre="Ana", apellido="Gomez", email="ana@test.com",
            usuario=self.user_vis, fecha_registro=date.today(),
        )




class AprobarInscripcionViewTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Tecnologia", descripcion="Desc")
        self.feria = Feria.objects.create(
            nombre="Feria Tech", categoria=self.categoria,
            fecha_inicio=date.today() + timedelta(days=5),
            fecha_fin=date.today() + timedelta(days=7),
            ubicacion="Ushuaia", capacidad_puestos=10,
        )
        self.user_emp = User.objects.create_user(username="emp1", password="test1234")
        self.emprendedor = Emprendedor.objects.create(
            nombre="Juan", apellido="Perez", email="juan@test.com",
            rubro=self.categoria, telefono="123", usuario=self.user_emp,
        )
        self.inscripcion = Inscripcion.objects.create(
            emprendedor=self.emprendedor, feria=self.feria,
            estado="Lista_espera", registrado_por="admin",
        )

        self.user_admin = User.objects.create_user(username="admin1", password="test1234")
        permiso = Permission.objects.get(
            codename="change_inscripcion",
            content_type=ContentType.objects.get_for_model(Inscripcion),
        )
        self.user_admin.user_permissions.add(permiso)

    def test_usuario_sin_permiso_no_puede_aprobar(self):
        self.client.login(username="emp1", password="test1234")
        response = self.client.post(
            reverse('ferias:aprobar_inscripcion', args=[self.inscripcion.pk]),
            {'numero_puesto': 3}
        )
        self.assertEqual(response.status_code, 403)
        self.inscripcion.refresh_from_db()
        self.assertEqual(self.inscripcion.estado, "Lista_espera")  # no cambió

    def test_usuario_con_permiso_aprueba_correctamente(self):
        self.client.login(username="admin1", password="test1234")
        response = self.client.post(
            reverse('ferias:aprobar_inscripcion', args=[self.inscripcion.pk]),
            {'numero_puesto': 3}
        )
        self.inscripcion.refresh_from_db()
        self.assertEqual(self.inscripcion.estado, "Confirmada")
        self.assertEqual(self.inscripcion.numero_puesto, 3)
        self.assertRedirects(response, reverse('ferias:perfil'))

    def test_sin_numero_puesto_no_aprueba(self):
        self.client.login(username="admin1", password="test1234")
        response = self.client.post(
            reverse('ferias:aprobar_inscripcion', args=[self.inscripcion.pk]),
            {}  # sin numero_puesto
        )
        self.inscripcion.refresh_from_db()
        self.assertEqual(self.inscripcion.estado, "Lista_espera")  # no cambió


class CancelarInscripcionViewTest(TestCase):
    """
    NOTA: estos tests exponen un bug real en CancelarInscripcionView.post():
    usa estado='Confirmada' en vez de estado='Cancelada'. Van a fallar
    hasta que se corrija esa línea en views.py.
    """

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Tecnologia", descripcion="Desc")
        self.feria = Feria.objects.create(
            nombre="Feria Tech", categoria=self.categoria,
            fecha_inicio=date.today() + timedelta(days=5),
            fecha_fin=date.today() + timedelta(days=7),
            ubicacion="Ushuaia", capacidad_puestos=10,
        )
        self.user_emp = User.objects.create_user(username="emp1", password="test1234")
        self.emprendedor = Emprendedor.objects.create(
            nombre="Juan", apellido="Perez", email="juan@test.com",
            rubro=self.categoria, telefono="123", usuario=self.user_emp,
        )
        self.inscripcion = Inscripcion.objects.create(
            emprendedor=self.emprendedor, feria=self.feria,
            estado="Lista_espera", registrado_por="admin",
        )

        self.user_otro_emp = User.objects.create_user(username="emp2", password="test1234")
        Emprendedor.objects.create(
            nombre="Pedro", apellido="Lopez", email="pedro@test.com",
            rubro=self.categoria, telefono="456", usuario=self.user_otro_emp,
        )

    def test_dueño_de_inscripcion_puede_cancelar(self):
        self.client.login(username="emp1", password="test1234")
        self.client.post(reverse('ferias:cancelar_inscripcion', args=[self.inscripcion.pk]))
        self.inscripcion.refresh_from_db()
        self.assertEqual(self.inscripcion.estado, "Cancelada")

    def test_otro_emprendedor_no_puede_cancelar_inscripcion_ajena(self):
        self.client.login(username="emp2", password="test1234")
        response = self.client.post(reverse('ferias:cancelar_inscripcion', args=[self.inscripcion.pk]))
        self.assertEqual(response.status_code, 302)  # handle_no_permission redirige
        self.inscripcion.refresh_from_db()
        self.assertEqual(self.inscripcion.estado, "Lista_espera")