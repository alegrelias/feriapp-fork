# app/management/commands/cargar_datos_prueba.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta

from app.models import Categoria, Feria, Emprendedor, Visitante, Inscripcion, Resenia


class Command(BaseCommand):
    help = "Carga datos de prueba para la demo de FeriApp"

    def handle(self, *args, **options):
        hoy = timezone.now().date()

        # --- CATEGORÍAS ---
        cat_gastro = Categoria.objects.create(nombre="Gastronomía", descripcion="Comidas y bebidas")
        cat_artesanias = Categoria.objects.create(nombre="Artesanías", descripcion="Productos hechos a mano")
        cat_tech = Categoria.objects.create(nombre="Tecnología", descripcion="Productos y servicios tecnológicos")

        # --- FERIAS ---
        feria_proxima = Feria.objects.create(
            nombre="Feria de Primavera",
            categoria=cat_gastro,
            fecha_inicio=hoy + timedelta(days=15),
            fecha_fin=hoy + timedelta(days=17),
            ubicacion="Parque Central",
            capacidad_puestos=20,
        )

        feria_en_curso = Feria.objects.create(
            nombre="Expo Artesanal",
            categoria=cat_artesanias,
            fecha_inicio=hoy - timedelta(days=1),
            fecha_fin=hoy + timedelta(days=3),
            ubicacion="Plaza San Martín",
            capacidad_puestos=10,
        )

        feria_finalizada = Feria.objects.create(
            nombre="Feria Tech 2026",
            categoria=cat_tech,
            fecha_inicio=hoy - timedelta(days=30),
            fecha_fin=hoy - timedelta(days=27),
            ubicacion="Centro de Convenciones",
            capacidad_puestos=15,
        )

        # --- USUARIOS EMPRENDEDORES ---
        user_emp1 = User.objects.create_user(username="emprendedor1", password="test1234")
        emp1 = Emprendedor.objects.create(
            nombre="Juan", apellido="Pérez", email="juan@test.com",
            rubro=cat_gastro, telefono="3814000001", usuario=user_emp1,
        )

        user_emp2 = User.objects.create_user(username="emprendedor2", password="test1234")
        emp2 = Emprendedor.objects.create(
            nombre="María", apellido="López", email="maria@test.com",
            rubro=cat_artesanias, telefono="3814000002", usuario=user_emp2,
        )

        user_emp3 = User.objects.create_user(username="emprendedor3", password="test1234")
        emp3 = Emprendedor.objects.create(
            nombre="Carlos", apellido="Ruiz", email="carlos@test.com",
            rubro=cat_tech, telefono="3814000003", usuario=user_emp3,
        )

        # --- USUARIOS VISITANTES ---
        user_vis1 = User.objects.create_user(username="visitante1", password="test1234")
        vis1 = Visitante.objects.create(
            nombre="Ana", apellido="Gómez", email="ana@test.com",
            usuario=user_vis1, fecha_registro=hoy - timedelta(days=60),
        )

        user_vis2 = User.objects.create_user(username="visitante2", password="test1234")
        vis2 = Visitante.objects.create(
            nombre="Pedro", apellido="Díaz", email="pedro@test.com",
            usuario=user_vis2, fecha_registro=hoy - timedelta(days=10),
        )

        # --- SUPERUSUARIO ADMIN (para /admin y para aprobar inscripciones) ---
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(username="admin", password="admin1234", email="admin@test.com")

        # --- INSCRIPCIONES (usando Inscripcion.objects.create directo, sin pasar por validate,
        # porque acá nosotros como "dueños" de los datos ya garantizamos consistencia) ---

        # Confirmada, con puesto
        Inscripcion.objects.create(
            emprendedor=emp1, feria=feria_en_curso, numero_puesto=1,
            estado="Confirmada", registrado_por="admin",
        )

        # Lista de espera, sin puesto (para mostrar el flujo de aprobar)
        Inscripcion.objects.create(
            emprendedor=emp2, feria=feria_en_curso,
            estado="Lista_espera", registrado_por="emprendedor2",
        )

        # Otra en lista de espera, en otra feria
        Inscripcion.objects.create(
            emprendedor=emp3, feria=feria_proxima,
            estado="Lista_espera", registrado_por="emprendedor3",
        )

        # Cancelada, para mostrar ese estado también
        Inscripcion.objects.create(
            emprendedor=emp1, feria=feria_finalizada, numero_puesto=5,
            estado="Cancelada", registrado_por="admin",
        )

        # --- RESEÑAS ---
        Resenia.objects.create(
            visitante=vis1, feria=feria_finalizada, calificacion=5,
            comentario="Excelente organización y variedad de stands.",
        )
        Resenia.objects.create(
            visitante=vis1, feria=feria_en_curso, calificacion=4,
            comentario="Muy buena, aunque faltó más espacio entre puestos.",
        )
        Resenia.objects.create(
            visitante=vis2, feria=feria_finalizada, calificacion=3,
            comentario="Estuvo bien, esperaba más variedad.",
        )

        self.stdout.write(self.style.SUCCESS("Datos de prueba cargados correctamente."))
        self.stdout.write(self.style.WARNING(
            "\nUsuarios de prueba:\n"
            "  admin / admin1234 (superuser)\n"
            "  emprendedor1 / test1234 (Juan Pérez)\n"
            "  emprendedor2 / test1234 (María López)\n"
            "  emprendedor3 / test1234 (Carlos Ruiz)\n"
            "  visitante1 / test1234 (Ana Gómez)\n"
            "  visitante2 / test1234 (Pedro Díaz)\n"
        ))