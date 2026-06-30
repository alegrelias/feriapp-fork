"""Vistas públicas de la aplicación de ferias."""

from django.views.generic import ListView, TemplateView, DetailView, CreateView, View
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import  Avg
from django.db.models.functions import Round
from .models import Feria, Emprendedor,Inscripcion,Categoria,Resenia,Visitante
from datetime import date
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import FeriaForm, RegistroEmprendedorForm,RegistroVisitanteForm
from .forms import InscripcionForm
from django.contrib import messages
from django.db import transaction



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



        context["promedio_resenias"] = stat.get("avg") or 0
        context["ferias_activas"] = Feria.objects.filter(activa=True).order_by("-fecha_inicio")[:5]

        return context


class PerfilView(LoginRequiredMixin,TemplateView):
    template_name = "ferias/perfil.html"
    permission_required = 'app.change_inscripcion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emprendedor = None
        visitante = None
        context["inscripciones_a_evaluar"] = Inscripcion.objects.filter(estado__in=["Lista_espera", "Confirmada"])
        try:
            emprendedor = self.request.user.emprendedor  #  acceder al emprendedor
        except:
             # si no tiene emprendedor, Django lanza un error
            # en vez de explotar, intentamos con visitante
            try:
                visitante = self.request.user.visitante
            except:
             # si tampoco tiene visitante (ej: admin)
                perfil = self.request.user


        if emprendedor:
            #inscripciones_emprendedor es el related name que se le inyecta como atributo a emprendedor
            #SELECT * FROM mi_app_inscripcion WHERE emprendedor_id = [ID del emprendedor actual];
            #  con select related hace el join con Feria para evitar viajar 2 veces a la bd
            context["inscripciones"] = emprendedor.inscripciones_emprendedor.select_related('feria')
            context["perfil"] = emprendedor
            context["tipo"] = "Emprendedor"

        elif visitante:
            context["resenias"] = visitante.resenias.select_related('feria')
            context["perfil"] = visitante
            context["tipo"] = "Visitante"
        else:
             context["perfil"] = perfil

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
        emprendedor = None
        visitante = None
        try:
            emprendedor = self.request.user.emprendedor  #  acceder al emprendedor
        except:

            try:
                visitante = self.request.user.visitante
            except:

                perfil = self.request.user

        inscripciones = Inscripcion.objects.filter(
            feria=self.object,
            estado="Confirmada"
        )

        context["inscripciones"] = inscripciones
        context["emprendedor"] = emprendedor
        context["visitante"] = visitante

        context["ocupacion"] = (self.object.puestos_ocupados() * 100) / self.object.capacidad_puestos

        #self.object es la pk de la url
        context["resenias"] = Resenia.objects.filter(feria=self.object)

        return context

    def post(self, request, *args, **kwargs):
        #self.object funciona si se hace un get, para post hace una consutla a la bd
        feria = self.get_object()
        comentario = request.POST.get("comentario")
        calificacion = request.POST.get("calificacion")
        visitante = None

        try:
            visitante = self.request.user.visitante
        except:

            messages.warning(self.request, "Solo los visitantes pueden dejar reseñas")
            return redirect("ferias:detalle_feria", pk=feria.pk)


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

class NuevaFeriaView(PermissionRequiredMixin,SuccessMessageMixin, CreateView):

    template_name = "ferias/nueva_feria.html"
    form_class = FeriaForm
    success_url = reverse_lazy('ferias:lista_ferias')
    permission_required = 'app.add_feria'
    success_message = "¡La feria se ha creado de manera exitosa!"

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
class RegistroView(TemplateView):
    template_name = 'ferias/registration/registro.html'
class RegistroEmprendedorView(CreateView):
    template_name = 'ferias/registration/registro_emprendedor.html'
    form_class = RegistroEmprendedorForm
    success_url = reverse_lazy('ferias:login')

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save()  # crea el User
            Emprendedor.objects.create(
                usuario=user,
                nombre=form.cleaned_data["nombre"],
                apellido=form.cleaned_data["apellido"],
                email=form.cleaned_data["email"],
                telefono=form.cleaned_data["telefono"],
                rubro=form.cleaned_data["rubro"]
            )
        messages.success(self.request, "Registro como Emprendedor exitoso, inicie sesión")
        return redirect(self.success_url)

class RegistroVisitanteView(CreateView):
    template_name = 'ferias/registration/registro_visitante.html'
    form_class = RegistroVisitanteForm
    success_url = reverse_lazy('ferias:login')




    def form_valid(self, form):
        with transaction.atomic():
            user = form.save()
            Visitante.objects.create(
                usuario=user,
                nombre=form.cleaned_data["nombre"],
                apellido=form.cleaned_data["apellido"],
                email=form.cleaned_data["email"],
                fecha_registro=date.today()
            )
        messages.success(self.request, "Registro como Visitante exitoso, inicia sesión")
        return redirect(self.success_url)



class NuevaInscripcionView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Inscripcion
    form_class = InscripcionForm
    template_name = 'ferias/nueva_inscripcion.html'

    def test_func(self):

        # si el usuario tiene atributo emprendedor, Si da False, el motor de Django hace: 'self.handle_no_permission()'
        return hasattr(self.request.user, 'emprendedor')

    def handle_no_permission(self):
        """
         se ejeecuta solo si test_func() devuelve False

        """
        messages.warning(self.request, "Acceso denegado: Debes registrar un perfil de Emprendedor para inscribirte.")

        return redirect("ferias:lista_ferias")

    def form_valid(self, form):
        inscripcion = form.save(commit=False)  # crea el objeto pero NO lo guarda todavía
        inscripcion.feria = Feria.objects.get(pk=self.kwargs["pk"])
        inscripcion.emprendedor = self.request.user.emprendedor
        inscripcion.registrado_por = inscripcion.emprendedor
        errors = Inscripcion.validate(emprendedor=inscripcion.emprendedor, feria=inscripcion.feria,
        numero_puesto=inscripcion.numero_puesto, registrado_por=inscripcion.registrado_por, estado=inscripcion.estado)
        if errors:
            form.add_error(None, errors)
            return self.form_invalid(form)
        inscripcion.save()                     # ahora sí se guarda
        messages.success(self.request, "Tu inscripción se encuentra en lista de espera. Cuando sea confirmada, recibirás un correo electrónico con la información correspondiente.")

        return redirect("ferias:lista_ferias")  # redirige a la lista de ferias


class CancelarInscripcionView(LoginRequiredMixin, UserPassesTestMixin, View):
    model = Inscripcion
    template_name = 'ferias/cancelar_inscripcion.html'
    success_url = reverse_lazy('ferias:perfil')

    def test_func(self):
        inscripcion = get_object_or_404(Inscripcion, pk=self.kwargs.get('pk'))

        if not hasattr(self.request.user, 'emprendedor'):
            return False

        return inscripcion.emprendedor == self.request.user.emprendedor

    def handle_no_permission(self):
        messages.error(self.request, "No tenés permiso para cancelar una inscripción que no es tuya.")
        return redirect('ferias:perfil')

    def post(self, request, *args, **kwargs):
        inscripcion = get_object_or_404(Inscripcion, pk=self.kwargs.get('pk'))
        inscripcion.estado = "Cancelada"
        inscripcion.save()
        messages.success(self.request, "Inscripción cancelada exitosamente.")
        return redirect(self.success_url)

    def get_object(self, queryset=None):
        inscripcion_id = self.kwargs.get('pk')
        return Inscripcion.objects.get(pk=inscripcion_id)


class AprobarInscripcionRapidaView(PermissionRequiredMixin, View):
    permission_required = 'app.change_inscripcion'

    def post(self, request, *args, **kwargs):
        # Tomamos el ID de la URL o del POST
        inscripcion = get_object_or_404(Inscripcion, pk=self.kwargs['pk'])
        inscripcion.estado = 'APROBADA'
        inscripcion.save()
        
        messages.success(request, f"Inscripción aprobada con éxito.")
        # Te manda de vuelta al perfil de donde viniste
        return redirect('ferias:perfil')

