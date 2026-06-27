"""Vistas públicas de la aplicación de ferias."""

from django.views.generic import ListView, TemplateView, DetailView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Avg, Sum, Max, Min
from django.db.models.functions import Round 
from .models import Feria, Emprendedor,Inscripcion, Categoria,Resenia,Visitante
from datetime import date
from django.shortcuts import redirect



class HomeView(TemplateView):
    """Vista de inicio. completar con estadísticas."""

    template_name = "ferias/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoy = date.today()
        stat = Resenia.objects.aggregate(avg = Round(Avg("calificacion"),1))

        context["total_ferias_activas"] = Feria.objects.filter(fecha_inicio=hoy).count()
        context["total_emprendedores"] = Emprendedor.objects.count()
        context[hoy] =timezone.now().date()
        #__gte greater than or equal 
        context["ferias_proximas"] = Feria.objects.filter(fecha_inicio__gte=hoy).count()
        context["inscripciones_confirmadas"] = Inscripcion.objects.filter(estado="Confirmada").count()
        context["resenias"] = Resenia.objects.all()[:5]
        context["total_ferias_realizadas"] = Feria.objects.filter(fecha_inicio__lte=hoy).count()



        context["promedio_resenias"] = stat.get("avg",[])
        context["ferias_activas"] = Feria.objects.filter(activa=True).order_by("-fecha_inicio")[:5]

        return context


class PerfilView(LoginRequiredMixin,TemplateView):
    template_name = "perfil.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emprendedor = Emprendedor.objects.filter(usuario=self.request.user).first()
        visitante = Visitante.objects.filter(usuario=self.request.user).first()
        

        if emprendedor:
            #inscripciones_emprendedor es el related name que se le inyecta como atributo a emprendedor
            #SELECT * FROM mi_app_inscripcion WHERE emprendedor_id = [ID del emprendedor actual];
            #  con select related hace el join con Feria para evitar viajar 2 veces a la bd
            context["inscripciones"] = emprendedor.inscripciones_emprendedor.select_related('feria')
            context["perfil"] = emprendedor
            context["tipo"] = "emprendedor"
           
        elif visitante:
            context["perfil"] = visitante
            context["tipo"] = "visitante"
        
        return context



# ========== Vistas para Ferias ==========

class FeriasListView(LoginRequiredMixin, ListView):
    """Lista todas las ferias activas."""

    model = Feria
    template_name = "ferias/lista_ferias.html"
    context_object_name = "ferias"

    def get_queryset(self):
        """Retorna solo las ferias marcadas como activas."""
        queryset = Feria.objects.filter(activa=True)

        categoria_id = self.request.GET.get("categoria")

        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["categorias"] = Categoria.objects.all()

        return context

class FeriasDetailView(LoginRequiredMixin, DetailView):
    model = Feria
    template_name = 'ferias/ferias_detail_view.html'
    context_object_name = 'feria'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        inscripciones = Inscripcion.objects.filter(
            feria=self.object,
            estado="Confirmada"
        )

        context["inscripciones"] = inscripciones

        context["ocupacion"] = (self.object.puestos_ocupados() * 100) / self.object.capacidad_puestos

        #self.object es la pk de la url
        context["resenias"] = Resenia.objects.filter(feria=self.object)

        return context
    
    def post(self, request, *args, **kwargs):
        #self.object funciona si se hace un get, para post hace una consutla a la bd
        feria = self.get_object()
        comentario = request.POST.get("comentario")
        calificacion = request.POST.get("calificacion")
        visitante = Visitante.objects.first()  # temporal
        
        #crea y guarda la reseña
        Resenia.objects.create(
            visitante=visitante,
            feria=feria,
            calificacion=calificacion,
            comentario=comentario
        )

        #redirige al detalle de la feria
        
        return redirect("ferias:detalle_feria", pk=feria.pk)



# ========== Vistas para Emprendedores ==========

class EmprendedoresListView(LoginRequiredMixin, ListView):
    model = Emprendedor
    template_name = 'ferias/emprendedores_list_view.html'
    context_object_name = 'emprendedores'

    def get_queryset(self):
        """Retorna los emprendedores activos"""
        return Emprendedor.objects.listar_ordenados()

# TODO: implementar las siguientes vistas:
# class NuevaFeriaView(CreateView): ...

class NuevaFeriaView(LoginRequiredMixin, CreateView):

    model = Feria

    fields = ["nombre","categoria","fecha_inicio","fecha_fin","ubicacion","capacidad_puestos","activa",]

    template_name = "ferias/nueva_feria.html"

    success_url = reverse_lazy("ferias:lista_ferias")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        form.fields['categoria'].empty_label = "Seleccione una categoría"
        
        for field_name, field in form.fields.items():
            if field_name == 'categoria':
                field.widget.attrs.update({'class': 'form-select'})
            elif field_name == 'activa':
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
                
        return form

# class NuevaInscripcionView(CreateView): ...
# class CancelarInscripcionView(View): ...

class RegistroUsuarioView(CreateView):
    template_name = 'ferias/registration/registro.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('ferias:login')