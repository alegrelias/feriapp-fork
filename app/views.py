"""Vistas públicas de la aplicación de ferias."""

from django.views.generic import ListView, TemplateView

from .models import Feria


class HomeView(TemplateView):
    """Vista de inicio. Por ahora vacía — completar con estadísticas."""

    template_name = "ferias/home.html"


class ListaFeriasView(ListView):
    """Lista todas las ferias activas."""

    model = Feria
    template_name = "ferias/lista_ferias.html"
    context_object_name = "ferias"

    def get_queryset(self):
        """Retorna solo las ferias marcadas como activas."""
        return Feria.objects.filter(activa=True)


# TODO: implementar las siguientes vistas:
# class DetalleFeriaView(DetailView): ...
# class NuevaFeriaView(CreateView): ...
# class ListaEmprendedoresView(ListView): ...
# class NuevaInscripcionView(CreateView): ...
# class CancelarInscripcionView(View): ...
