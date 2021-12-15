from django.contrib import admin

# Register your models here.
from usuarios import models

admin.site.register(models.Usuario)
admin.site.register(models.Area)
admin.site.register(models.Tema)
admin.site.register(models.Pregunta)
admin.site.register(models.Respuesta)
admin.site.register(models.Nivel)
admin.site.register(models.Confiabilidad)
admin.site.register(models.Comentario)
admin.site.register(models.Calificacion)