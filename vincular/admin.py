from django.contrib import admin
from django.http import HttpResponseRedirect
from .models import RFID
from django.contrib import messages

# Register your models here.
@admin.register(RFID)
class RFIDAdmin(admin.ModelAdmin):
	
	def response_change(self, request, obj):        
		if "_activarlector" in request.POST:
		    obj.codigo = 12
		    obj.save()
		    self.message_user(request, "Se ha efectuado la lectura")
		    messages.error(request, 'Three credits sa in your account.')
		    return HttpResponseRedirect(".")
		return super().response_change(request, obj)

	def response_add(self, request, obj, post_url_continue=None):
		if "_activarlector" in request.POST:
		    obj.codigo = 15
		    obj.save()
		    self.message_user(request, "Se ha efectuado la lectura")
		return super().response_add(request, obj)