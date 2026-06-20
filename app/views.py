"""Vistas públicas de la aplicación de ferias."""

from django.views.generic import ListView, TemplateView, DetailView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.utils import timezone

from .models import Feria, Emprendedor,Inscripcion


class HomeView(TemplateView):
    """Vista de inicio. Por ahora vacía — completar con estadísticas."""

    template_name = "ferias/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoy = timezone.now().date()

        context["total_ferias_activas"] = Feria.objects.filter(activa=True).count()
        context["total_emprendedores"] = Emprendedor.objects.count()

        #__gte greater than or equal 
        context["ferias_proximas"] = Feria.objects.filter(fecha_inicio__gte=hoy).count()
        context["inscripciones_confirmadas"] = Inscripcion.objects.filter(estado="Confirmada").count()

        return context


# ========== Vistas para Ferias ==========

class FeriasListView(ListView):
    """Lista todas las ferias activas."""

    model = Feria
    template_name = "ferias/lista_ferias.html"
    context_object_name = "ferias"

    def get_queryset(self):
        """Retorna solo las ferias marcadas como activas."""
        return Feria.objects.filter(activa=True)

class FeriasDetailView(DetailView):
    model = Feria
    template_name = 'ferias/ferias_detail_view.html'
    context_object_name = 'feria'

# ========== Vistas para Emprendedores ==========

class EmprendedoresListView(ListView):
    model = Emprendedor
    template_name = 'ferias/emprendedores_list_view.html'
    context_object_name = 'emprendedores'

    def get_queryset(self):
        """Retorna los emprendedores activos"""
        return Emprendedor.objects.listar_ordenados()

# TODO: implementar las siguientes vistas:
# class NuevaFeriaView(CreateView): ...
# class NuevaInscripcionView(CreateView): ...
# class CancelarInscripcionView(View): ...

class RegistroUsuarioView(CreateView):
    template_name = 'ferias/registration/registro.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('ferias:login')