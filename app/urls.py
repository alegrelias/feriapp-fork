"""Definición de rutas públicas de la aplicación."""

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "ferias"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("ferias/", views.FeriasListView.as_view(), name="lista_ferias"),
    path("ferias/<int:pk>/", views.FeriasDetailView.as_view(), name="detalle_feria"),
    path("emprendedores/", views.EmprendedoresListView.as_view(), name="lista_emprendedores"),
    # TODO:
    path("ferias/nueva/", views.NuevaFeriaView.as_view(), name="nueva_feria"),
    # path("inscripciones/nueva/", views.NuevaInscripcionView.as_view(), name="nueva_inscripcion"),

    #LOGIN, LOGOUT y REGISTRO
    path('login/', auth_views.LoginView.as_view(template_name='ferias/registration/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='ferias:home'), name='logout'),
    path('registro/', views.RegistroUsuarioView.as_view(), name='registro'),
]
