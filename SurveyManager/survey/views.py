from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets,generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.http import HttpRequest,HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template import Context
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from .models import Encuesta,Pregunta,Respuesta,RespuestaPregunta,Carrera,Alumno,Generacion

# Create your views here.
def index(request):
	encuestas=Encuesta.objects.all()
	carreras=Carrera.objects.all()
	return render(request,'index.html',{'encuestas':encuestas,'carreras':carreras})

# Create your views here.
def Constructor(request):
	encuestas=Encuesta.objects.all()
	return render(request,'constructor.html',{'encuestas':encuestas})

# Create your views here.
def Egresados(request):
	carreras=Carrera.objects.all()
	generaciones=Generacion.objects.all()
	return render(request,'egresados.html',{'carreras':carreras,'generaciones':generaciones})

def GetEncuesta(request,id=1):
	encuesta=Encuesta.objects.get(id=id)

	return render(request,'encuesta.html',{"encuesta":encuesta})

def Responder(request):
	idEncuesta=request.GET['encuesta']
	idAlumno=request.GET['alumno']
	encuesta=Encuesta.objects.get(id=idEncuesta)
	alumno=Alumno.objects.get(id=idAlumno)
	pregunta=Pregunta.objects.filter(encuesta=encuesta)
	status=RespuestaPregunta.objects.filter(alumno=idAlumno,pregunta=pregunta[0])
	print(status)
	if status:
		encuesta.estatus=1
	else:
		encuesta.estatus=2
	
	print(encuesta)
	print(alumno)

	return render(request,'responder.html',{"encuesta":encuesta,"alumno":alumno,"preguntas":pregunta})


def Respuestas(request,id=1):
	preguntas=Pregunta.objects.filter(encuesta=id)
	encuesta=Encuesta.objects.get(id=id)
	print(preguntas)
	
	for pregunta in preguntas:
		print(pregunta)
		respuesta=[]
		if pregunta.tipo==1:
			posible_respuestas=Respuesta.objects.filter(pregunta=pregunta)
			for resp in posible_respuestas:
				respuesta_pregunta=RespuestaPregunta.objects.filter(pregunta=pregunta,respuesta=resp)
				print(respuesta_pregunta)
				temp={"respuesa":resp.valor,"numero":len(respuesta_pregunta)}
				print(temp)
				respuesta.append(temp)
		else:
			respuesta_pregunta=RespuestaPregunta.objects.filter(pregunta=pregunta,respuesta=resp)
			respuesta.append(respuesta_pregunta)
		
		pregunta.respuestas=respuesta
		print(pregunta)

			
	print(preguntas)
	return render(request,'respuestas.html',{"respuestas":preguntas,"encuesta":encuesta})

#API

class Survey(APIView):
	def get(self,request):
		opcion=request.GET['opcion']
		#1=>TODAS LAS ENCUESTAS
		#2=>SOLO UNA
		print(opcion)
		encuestas={}
		if opcion=='1':
			encuestas=Encuesta.objects.all()
		else:
			id=request.GET["id"]
			encuestas=Encuesta.objects.filter(id=id)
		print(encuestas)
		response_data={}
		response_data['message'] = serializers.serialize('json', encuestas)
		
		return HttpResponse(JsonResponse(response_data), content_type="application/json")
		

	def post(self,request):
		print(request.data)
		nombre=request.data["nombre"]
		descripcion=request.data["descripcion"]
		estructura=request.data["estructura"]
		encuesta = Encuesta(nombre=nombre,descripcion=descripcion,estructura=estructura)
		encuesta.save()
		encuestaId=Encuesta.objects.latest('id')
		print(encuestaId.id)
		return Response({'error':1,'encuesta':encuestaId.id})

class SaveQuestion(APIView):
	def post(self,request):
		print(request.data)
		descripcion=request.data["descripcion"]
		encuestaId=request.data["encuesta"]
		tipo=request.data["tipo"]
		json_id=request.data["json_id"]
		encuesta=Encuesta.objects.get(id=encuestaId)
		pregunta = Pregunta(descripcion=descripcion,encuesta=encuesta,tipo=tipo,json_id=json_id)
		pregunta.save()
		preguntaId=Pregunta.objects.latest('id')
		
		return Response({'error':1,'pregunta':preguntaId.id})

class SaveAnswer(APIView):
	def get(self,request):
		encuestaId=request.GET['encuesta']
		preguntas=Pregunta.objects.filter(encuesta=encuestaId)
		preguntaJson=[]
		for pregunta in preguntas:
			print(pregunta)
			respuesta=[]
			total=0
			if pregunta.tipo==1:
				posible_respuestas=Respuesta.objects.filter(pregunta=pregunta)
				
				for resp in posible_respuestas:
					respuesta_pregunta=RespuestaPregunta.objects.filter(pregunta=pregunta,respuesta=resp)
					total+=len(respuesta_pregunta)
					temp={"respuesta":resp.valor,"numero":len(respuesta_pregunta)}
					respuesta.append(temp)
			else:
				respuesta_pregunta=RespuestaPregunta.objects.filter(pregunta=pregunta,respuesta=resp)
				respuesta.append(respuesta_pregunta)


			temp2={"pregunta_id":pregunta.id,"numero_pregunta":pregunta.numero,"pregunta":pregunta.descripcion,"total":total,"tipo":pregunta.tipo,"respuestas":respuesta}
			preguntaJson.append(temp2)
			print(preguntaJson)

		
		
		return Response({"message":preguntaJson})

	def post(self,request):
		print(request.data)
		valor=request.data["valor"]
		preguntaId=request.data["pregunta"]
		json_id=request.data["json_id"]
		pregunta=Pregunta.objects.get(id=preguntaId)
		respuesta = Respuesta(valor=valor,pregunta=pregunta,json_id=json_id)
		respuesta.save()
		respuestaId=Respuesta.objects.latest('id')
		
		return Response({'error':1,'respuesta':respuestaId.id})

class DeleteQuestion(APIView):
	def post(self,request):
		print(request.data)
		encuestaId=request.data["encuesta"]
		Encuesta.objects.get(id=encuestaId).delete()
		
		return Response({'error':1})

class MandarCorreo(APIView):
	def post(self,request):
		print(request.data)
		encuestaId=request.data["encuesta"]
		carreraId=request.data["carrera"]

		encuesta=Encuesta.objects.get(id=encuestaId)
		alumnos=Alumno.objects.filter(carrera=carreraId)
		for alumno in alumnos:
			print(alumno.email)
			
			ctx = {'encuesta': encuestaId,'alumno': alumno.id}
			html_content = render_to_string('email.html',ctx)
			message=strip_tags(html_content)
			subject='Encuesta'
			#message='podrias contestar la siguiente encuesta?'
			from_email=settings.EMAIL_HOST_USER
			to=[alumno.email]
			msg = EmailMultiAlternatives(subject, message, from_email, to)
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			

		
		return Response({'error':1})

class GetAnswers(APIView):
	def get(self,request):
		encuestaId=request.GET['encuesta']
		preguntas=Pregunta.objects.filter(encuesta=encuestaId)
		for pregunta in preguntas:
			print(pregunta)
			respuesta=[]
			if pregunta.tipo==1:
				posible_respuestas=Respuesta.objects.filter(pregunta=pregunta)
				for resp in posible_respuestas:
					respuesta_pregunta=RespuestaPregunta.objects.filter(pregunta=pregunta,respuesta=resp)
					print(respuesta_pregunta)
					temp={"respuesa":resp.valor,"numero":len(respuesta_pregunta)}
					print(temp)
					respuesta.append(temp)
			else:
				respuesta_pregunta=RespuestaPregunta.objects.filter(pregunta=pregunta,respuesta=resp)
				respuesta.append(respuesta_pregunta)

			pregunta.respuestas=respuesta

		response_data={}
		response_data['message'] = serializers.serialize('json', preguntas)
		
		return HttpResponse(JsonResponse(response_data), content_type="application/json")


class GetAlumnos(APIView):
	def get(self,request):
		carreraId=request.GET['carrera']
		carrera=Carrera.objects.get(id=carreraId)
		alumnos=Alumno.objects.filter(carrera=carrera)
		

		response_data={}
		response_data['message'] = serializers.serialize('json', alumnos)
		
		return HttpResponse(JsonResponse(response_data), content_type="application/json")

	def post(self,request):
		carreraId=request.data['carrera']
		nombre=request.data['nombre']
		apellidos=request.data['apellidos']
		email=request.data['email']
		
		carrera=Carrera.objects.get(id=carreraId)
		
		alumno = Alumno(nombre=nombre,apellidos=apellidos,email=email,carrera=carrera)
		alumno.save()
		return Response({'error':1})
		

class GuardarRespuesta(APIView):
	def post(self,request):
		json_id=request.data["name"]
		value=request.data["value"]
		alumnoId=request.data["alumno"]
		alumno=Alumno.objects.get(id=alumnoId)
		pregunta=Pregunta.objects.get(json_id=json_id)
		respuesta=Respuesta.objects.get(json_id=value)
		
		respuesta = RespuestaPregunta(alumno=alumno,pregunta=pregunta,respuesta=respuesta)
		respuesta.save()
		
		return Response({'error':1})

class GuardarCarrera(APIView):
	def post(self,request):
		generacionId=request.data["generacion"]
		nombre=request.data["nombre"]
		generacion=Generacion.objects.get(id=generacionId)
		
		carrera = Carrera(nombre=nombre,generacion=generacion)
		carrera.save()
		
		return Response({'error':1})

