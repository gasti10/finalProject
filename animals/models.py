from django.db import models
# Create your models here.

from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import datetime

class Animal(models.Model):
    """
    Modelo que representa un animal.
    """

    id = models.AutoField('Animal',primary_key=True)

    sexo = models.CharField('Sexo', help_text="M --> Macho & H --> Hembra", null=False, max_length=5)

    raza = models.CharField(max_length=100, help_text="Ingrese la raza si lo considera necesario")

    tipo = models.CharField(default="Bovino",max_length=100, help_text="Bovino - Ovino - Porcino", null=False)
    
    fecha_nac = models.DateField('Fecha de nacimiento',default=datetime.date.today,help_text="Ingrese la fecha de nacimiento")

    edad = models.IntegerField('Edad en dias',default=1, help_text="Se autocompleta a partir de la fecha indicada como nacimiento")

    caravana = models.OneToOneField('Caravana',on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """
        String que representa al objeto Animal
        """
        return self.tipo + " - Caravana Nro " + str(self.caravana.numero)

    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animales"
        ordering = ["-caravana"]    

class Caravana(models.Model):
    """
    Modelo que representa una Caravana.
    """

    numero = models.IntegerField(primary_key=True, null=False)

    CUIG = models.CharField(help_text="La obtención de la Clave Única de Identificación Ganadera (CUIG) es un requisito indispensable para adquirir las nuevas caravanas, que identificarán a los animales en forma individual.", max_length=100)

    RENSPA = models.CharField(max_length=100, help_text="El RENSPA es un registro obligatorio para todas las actividades de producción primaria del sector agrario. El responsable sanitario de la actividad debe aclarar sus datos personales, los del establecimiento y los datos de la explotación.")
    
    codRFID = models.OneToOneField('vincular.RFID',on_delete=models.SET_NULL,help_text="Seleccione el codigo de RFID", null=True)

    COLOR_CHOICES = [('1', ('Azul')), 
                     ('2', ('Amarillo')),
                     ('3', ('Rojo')),
                     ('4', ('Verde'))]

    color = models.CharField('Color', default="Azul", max_length=100, help_text="Ingrese el color de la caravana",choices=COLOR_CHOICES)
    
    def __str__(self):
        """
        String que representa al objeto Caravana
        """
        return "Nro "+ str(self.numero) + " - CUIG=" + self.CUIG
    
    
    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Caravana
        """
        return reverse('Caravana-detail', args=[str(self.numero)])

    class Meta:
        verbose_name = "Caravana"
        verbose_name_plural = "Caravanas"
        ordering = ["-numero"]     

class Vacuna(models.Model):
    """
    Modelo que representa una Vacuna.
    """

    id = models.AutoField(primary_key=True)

    tipo = models.CharField(help_text="Ingrese el tipo de la vacuna", max_length=100)

    def __str__(self):
        """
        String que representa al objeto Vacuna
        """
        return self.tipo
    
    
    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Vacuna
        """
        return reverse('Vacuna-detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Vacuna"
        verbose_name_plural = "Vacunas"
        ordering = ["-id"]

class AnimalVacunado(models.Model):
    """
    Modelo que representa un Animal con Vacuna.
    """

    id = models.AutoField(primary_key=True)

    animal = models.ForeignKey('Animal',on_delete=models.SET_NULL, null=True)

    vacuna = models.ForeignKey('Vacuna',on_delete=models.SET_NULL, null=True)



    def __str__(self):
        """
        String que representa al objeto AnimalVacunado
        """
        return self.animal.tipo + " Nro " + str(self.animal.caravana_id.numero) + " vacunado con " + self.vacuna.tipo
    
    
    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de AnimalVacunado
        """
        return reverse('Animal Vacunado -detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Animal vacunado"
        verbose_name_plural = "Animales vacunados"
        ordering = ["-animal"]