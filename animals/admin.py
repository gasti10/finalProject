from django.contrib import admin

from .models import Animal, Caravana, Vacuna, AnimalVacunado

# Register your models here.

#admin.site.register(Animal)
admin.site.register(Caravana)
admin.site.register(Vacuna)
admin.site.register(AnimalVacunado)

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    actions = ['aplicarVacuna_GripeA']

    def aplicarVacuna_GripeA(self, request, queryset):
       	num = Vacuna.objects.count()+1
       	for anim in queryset:
            AnimalVacunado.objects.create( animal=anim, vacuna=Vacuna.objects.get(id=num))
    aplicarVacuna_GripeA.short_description = 'Aplicar Vacuna contra COVID-19'