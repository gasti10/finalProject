from django.shortcuts import render

# Create your views here.

from .models import *

def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    num_animales=Animal.objects.all().count()
    num_caravanas=Caravana.objects.all().count()
    # Libros disponibles (status = 'a')
    #num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_vacunas=Vacuna.objects.count()  # El 'all()' esta implícito por defecto.
    
    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'index.html',
        context={'num_animales':num_animales,'num_caravanas':num_caravanas,'num_vacunas':num_vacunas},
    )

from django.views import generic

class BovinoListView(generic.ListView):
    model = Animal
    # Filtra por animales de tipo "bovino"
    queryset = Animal.objects.filter(tipo__icontains='bovino')
    # Your own name for the list as a template variable
    context_object_name = 'bovinos'   
    # Specify your own template name/location
    template_name = 'bovinos.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BovinoListView, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['vacunas'] = Vacuna.objects.all()
        # Obtengo todas las vacunas que tienen los animales y lo ordeno
        context['animalesVacunados'] = AnimalVacunado.objects.all() 
        context['tiene'] = 0 
        return context  