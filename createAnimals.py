# python manage.py shell

from animals.models import *    


for i in range(1, 101):
    num = 1217 + i
    c = Caravana.objects.create(numero=num, CUIG="AA 420" , RENSPA="8888", codRFID = num )
    a = Animal.objects.create(sexo='M', raza="Vogelsberger Rund", caravana_id=c)

prueba = "hola"
print(prueba)