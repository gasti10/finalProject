from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns

# Create your models here.

class RFID(models.Model):
    """
    Modelo que representa un Chip RFID.
    """
    readonly_fields = ('created', 'updated')
    
    id = models.AutoField(primary_key=True)

    codigo = models.IntegerField('Codigo de Chip',help_text="Codigo de Chip", default=0)

    def __str__(self):
        """
        String que representa al objeto RFID
        """
        if self.codigo == 0:
        	rta = "Numero de Chip NO asignado"
        else:
        	rta = str(self.codigo)	
        return rta

    def get_absolute_url(self):
	    """
	     Devuelve la url para acceder a una instancia particular del modelo.
	    """
	    return reverse('model-detail-view', args=[str(self.id)])    
    
    class Meta:
        verbose_name = "RFID"
        verbose_name_plural = "RFIDs"
        ordering = ["-id"]