"""Definición de rutas públicas de la aplicación."""

from django.urls import path
from . import views

app_name = "ferias"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("ferias/", views.FeriasListView.as_view(), name="lista_ferias"),
    path("ferias/<int:pk>/", views.FeriasDetailView.as_view(), name="detalle_feria"),
    # TODO:
    # path("ferias/nueva/", views.NuevaFeriaView.as_view(), name="nueva_feria"),
    # path("emprendedores/", views.ListaEmprendedoresView.as_view(), name="lista_emprendedores"),
    # path("inscripciones/nueva/", views.NuevaInscripcionView.as_view(), name="nueva_inscripcion"),
]
