from django.db import models

# Create your models here.
class Nivel(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length = 255, null = True)
    fecha_de_creacion = models.DateTimeField(blank = True, null = True)
    fecha_de_modificacion = models.DateTimeField(blank = True, null = True)
    estado = models.BooleanField(null = True)

    def __str__(self):
        return self.nombre

class Area(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length = 255, null = True)
    fecha_de_creacion = models.DateTimeField(blank = True, null = True)
    fecha_de_modificacion = models.DateTimeField(blank = True, null = True)
    estado = models.BooleanField(null = True)

    def __str__(self):
        return self.nombre

class Tema(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length = 255, null = True)
    area = models.ForeignKey (Area, on_delete = models.CASCADE, null = True)
    fecha_de_creacion = models.DateTimeField(blank = True, null = True)
    fecha_de_modificacion = models.DateTimeField(blank = True, null = True)
    estado = models.BooleanField(null = True)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length = 50, null = True)
    usuario = models.CharField(max_length = 100, null = True)
    contrasenia = models.CharField(max_length = 255, null = True)
    correo = models.CharField(max_length = 100, null = True)
    celular = models.CharField(max_length = 20, null = True)
    pais = models.CharField(max_length = 50, null = True)
    fecha_de_nacimiento = models.DateTimeField(blank = True, null = True)
    nivel = models.ForeignKey (Nivel, on_delete = models.CASCADE, null = True)
    num_resp_confiables=models.IntegerField(null=True)
    fecha_de_creacion = models.DateTimeField(blank = True, null = True)
    fecha_de_modificacion = models.DateTimeField(blank = True, null = True)
    estado = models.BooleanField(null = True)

    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    id = models.AutoField(primary_key=True)
    enunciado = models.CharField(max_length = 500, null = True)
    descripcion = models.CharField(max_length = 500, null = True)
    usuario = models.ForeignKey (Usuario, on_delete = models.CASCADE, null = True)
    tema = models.ForeignKey (Tema, on_delete = models.CASCADE, null = True)
    area = models.ForeignKey (Area, on_delete = models.CASCADE, null = True)
    fecha_de_creacion = models.DateTimeField(blank = True, null = True)
    fecha_de_modificacion = models.DateTimeField(blank = True, null = True)
    estado = models.BooleanField(null = True)

    def __str__(self):
        return self.enunciado

class Confiabilidad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length = 255, null = True)
    fecha_de_creacion = models.DateTimeField(blank = True, null = True)
    fecha_de_modificacion = models.DateTimeField(blank = True, null = True)
    estado = models.BooleanField(null = True)

    def __str__(self):
        return self.nombre

class Respuesta(models.Model):
    id = models.AutoField(primary_key=True)
    contenido = models.CharField(max_length = 500, null = True)
    usuario = models.ForeignKey (Usuario, on_delete = models.CASCADE, null = True)
    pregunta = models.ForeignKey (Pregunta, on_delete = models.CASCADE, null = True)
    confiabilidad = models.ForeignKey (Confiabilidad, on_delete = models.CASCADE, null = True)
    aprobacion=models.IntegerField (null = True)
    num_buena_calificacion = models.IntegerField (null = True)
    num_mala_calificacion = models.IntegerField (null = True)
    fecha_de_creacion = models.DateTimeField(blank = True, null = True)
    fecha_de_modificacion = models.DateTimeField(blank = True, null = True)
    estado = models.BooleanField(null = True)

    def __str__(self):
        return self.contenido

class Comentario(models.Model):
    id = models.AutoField(primary_key=True)
    contenido = models.CharField(max_length = 500, null = True)
    usuario = models.ForeignKey (Usuario, on_delete = models.CASCADE, null = True)
    respuesta = models.ForeignKey (Respuesta, on_delete = models.CASCADE, null = True)
    comentario_id = models.IntegerField (null = True, blank = True)
    fecha_de_creacion = models.DateTimeField(blank = True, null = True)
    fecha_de_modificacion = models.DateTimeField(blank = True, null = True)
    estado = models.BooleanField(null = True)

    def __str__(self):
        return self.contenido

class Calificacion (models.Model):
    id = models.AutoField (primary_key = True)
    usuario = models.ForeignKey (Usuario, on_delete = models.CASCADE, null = True)
    respuesta = models.ForeignKey (Respuesta, on_delete = models.CASCADE, null = True)
    fecha_de_creacion = models.DateTimeField(blank = True, null = True)
    fecha_de_modificacion = models.DateTimeField(blank = True, null = True)
    estado = models.BooleanField(null = True)

    def __str__(self):
        return ""