from django.contrib import admin

# Register your models here.
from .models import Encuesta,Pregunta,Respuesta,Carrera,Generacion,Alumno,RespuestaPregunta
admin.site.register(Encuesta)
admin.site.register(Pregunta)
admin.site.register(Respuesta)
admin.site.register(RespuestaPregunta)
admin.site.register(Generacion)
admin.site.register(Carrera)
admin.site.register(Alumno)