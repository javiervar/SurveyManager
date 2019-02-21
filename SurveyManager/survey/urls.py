from django.urls import path
from survey import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns=[
	path('',views.index,name="index"),
	path('constructor/',views.Constructor,name="constructor"),
	path('egresados/',views.Egresados,name="egresados"),
	path('encuesta/<int:id>/',views.GetEncuesta,name="encuesta"),
	path('respuestas/<int:id>/',views.Respuestas,name="respuestas"),
	path('responder/',views.Responder,name="responder"),
	path('survey/',views.Survey.as_view(),name="survey"),
	path('saveQuestion/',views.SaveQuestion.as_view(),name="saveQuestion"),
	path('saveAnswer/',views.SaveAnswer.as_view(),name="saveAnswer"),
	path('deleteQuestion/',views.DeleteQuestion.as_view(),name="deleteQuestion"),
	path('getAlumnos/',views.GetAlumnos.as_view(),name="getAlumnos"),
	path('guardarRespuesta/',views.GuardarRespuesta.as_view(),name="guardarRespuesta"),
	path('guardarCarrera/',views.GuardarCarrera.as_view(),name="guardarCarrera"),
	path('enviar/',views.MandarCorreo.as_view(),name="enviar"),
	
]