from django.db import models

# Create your models here.
class Encuesta(models.Model):
	nombre=models.CharField(max_length=150)
	descripcion=models.TextField()
	estructura=models.TextField()
	fecha = models.DateTimeField(auto_now_add=True)

	
	def __str__(self):
		return str(self.nombre)


class Pregunta(models.Model):
	descripcion=models.CharField(max_length=150)
	encuesta = models.ForeignKey('Encuesta', on_delete=models.CASCADE)
	tipo=models.IntegerField(null=True)
	numero=models.IntegerField(default=1)
	json_id=models.CharField(max_length=50,null=True)
	
	def __str__(self):
		return str(self.descripcion)

class Respuesta(models.Model):
	valor=models.CharField(max_length=150)
	pregunta = models.ForeignKey('Pregunta', on_delete=models.CASCADE)
	json_id=models.CharField(max_length=50,null=True)
	def __str__(self):
		return str(self.valor)

class Carrera(models.Model):
	nombre=models.CharField(max_length=150)
	generacion = models.ForeignKey('Generacion', on_delete=models.CASCADE,null=True,blank=True)
	def __str__(self):
		return "%s %s" % (self.nombre, self.generacion)

class Generacion(models.Model):
	generacion=models.CharField(max_length=150,null=True,blank=True)
	def __str__(self):
		return str(self.generacion)

class Alumno(models.Model):
	email=models.CharField(max_length=100)
	nombre=models.CharField(max_length=100)
	apellidos=models.CharField(max_length=100)
	carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE)
	

	def __str__(self):
		return str(self.nombre)


class RespuestaPregunta(models.Model):
	respuesta = models.ForeignKey('Respuesta', on_delete=models.CASCADE)
	pregunta = models.ForeignKey('Pregunta', on_delete=models.CASCADE)
	alumno=models.ForeignKey('Alumno',on_delete=models.CASCADE,blank=True,null=True)
