"""Vistas públicas de la aplicación de ferias."""

from django.views.generic import ListView, TemplateView, DetailView

from .models import Feria, Emprendedor


class HomeView(TemplateView):
    """Vista de inicio. Por ahora vacía — completar con estadísticas."""

    template_name = "ferias/home.html"

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
