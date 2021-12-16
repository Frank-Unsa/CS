from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
#Formularios para en registro en django
from datetime import datetime as dt
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required

from django. contrib.auth import logout #jimy

from django.urls import reverse

# Create your views here.

from usuarios import models as usuarios
import datetime
from datetime import date, time #Jim

def foro(request):
    preguntas = list(usuarios.Pregunta.objects.all())
    temas = list(usuarios.Tema.objects.all())
    areas = list(usuarios.Area.objects.all())
    pregunta_usuario=[]
    for pregunta in preguntas:
        usuario=usuarios.Usuario.objects.get(id=pregunta.usuario_id)
        pregunta_usuario.append([pregunta,usuario])

    return render(request,'foro.html',{"preguntas": pregunta_usuario,"temas":temas,"areas":areas})

def pregunta(request):
    #recibimos el id de la pregunta seleccionada en foro
    temas = list(usuarios.Tema.objects.all())
    areas = list(usuarios.Area.objects.all())
    if request.GET.get("id",""):
        try:
            pregunta = usuarios.Pregunta.objects.get(id=request.GET.get('id',''))
            respuestas=()
        except ObjectDoesNotExist:
            return HttpResponse("Pregunta no encontrada")
    else:
        return HttpResponse("pregunta no encontrada")
    #verificamos que las respuestas a la pregunta sea confiable o no
    if request.GET.get("comun",""):
        respuestas = list(usuarios.Respuesta.objects.filter(pregunta_id=pregunta.id, confiabilidad_id = 1).order_by("-aprobacion"))       
        num_com_por_resp = []
        for r in respuestas:
            '''
            com_resp= list(usuarios.Comentario.objects.filter(respuesta_id=r.id, comentario_id= null))
            num_com_resp = len(com_resp)
            '''
            com= list(usuarios.Comentario.objects.filter(respuesta_id=r.id))
            usuario = usuarios.Usuario.objects.get(id=r.usuario_id)
            num_com_por_resp.append([r,len(com),usuario])     
        pregunta=usuarios.Pregunta.objects.get(id=request.GET.get("id",""))
        
        return render(request,'respuestas.html',{"respuestas":num_com_por_resp,"id_pregunta":pregunta})
    
    elif request.GET.get("confi",""):
        respuestas = list(usuarios.Respuesta.objects.filter(pregunta_id=pregunta.id, confiabilidad_id = 2).order_by("-aprobacion"))       
        num_com_por_resp = []
        for r in respuestas:
            com= list(usuarios.Comentario.objects.filter(respuesta_id=r.id))
            usuario = usuarios.Usuario.objects.get(id=r.usuario_id)
            num_com_por_resp.append([r,len(com),usuario]) 

        pregunta=usuarios.Pregunta.objects.get(id=request.GET.get("id",""))             
        return render(request,'respuestas.html',{"respuestas":num_com_por_resp,"id_pregunta":pregunta})
    
    respuestas = list(usuarios.Respuesta.objects.filter(pregunta_id=pregunta.id,confiabilidad_id = 2).order_by("-aprobacion"))
    num_com_por_resp = []
    for r in respuestas:
        com= list(usuarios.Comentario.objects.filter(respuesta_id=r.id))
        usuario = usuarios.Usuario.objects.get(id=r.usuario_id)
        num_com_por_resp.append([r,len(com),usuario])
    pregunta=usuarios.Pregunta.objects.get(id=request.GET.get("id",""))
    usuario_pregu=usuarios.Usuario.objects.get(id=pregunta.usuario_id)
    return render(request,'pregunta.html',{"pregunta":pregunta,"respuestas":num_com_por_resp,"temas":temas,"areas":areas,"id_pregunta":pregunta,"usuario_pregu":usuario_pregu})


def comentario(request):
    respuesta_id=request.GET.get("id_respuesta","")
    comentario_id=request.GET.get("id_comentario","")
    comentarios=[]
    if (not comentario_id):
        comentarios=list(usuarios.Comentario.objects.filter(respuesta_id = respuesta_id, comentario_id__isnull = True))
    else:
        comentarios=list(usuarios.Comentario.objects.filter(comentario_id = comentario_id))
    
    num_scom_com=[]

    for comentario in comentarios:
        com= list(usuarios.Comentario.objects.filter(comentario_id=comentario.id))
        usuario = usuarios.Usuario.objects.get(id=comentario.usuario_id)
        num_scom_com.append([comentario,len(com),usuario])
    return render(request,'comentario.html',{"comentarios":num_scom_com})

#likes y dislikes
def calificacion(request):
    usuario=request.GET.get("usuario","")
    usuario=usuarios.Usuario.objects.get(usuario=usuario)
    cal=request.GET["like"] if request.GET.get("like","") else request.GET["dislike"]
    respuesta=usuarios.Respuesta.objects.get(id=cal)
    if request.GET.get("like",""):
        if usuarios.Calificacion.objects.filter(usuario_id=usuario.id,respuesta_id=cal).exists():
            
            califi=list(usuarios.Calificacion.objects.filter(usuario_id=usuario.id,respuesta_id=cal))[0]
            
            if (califi.estado == True):
                respuesta.num_buena_calificacion=respuesta.num_buena_calificacion-1
                respuesta.save()
                califi.delete()
            else:
                califi.estado = True
                respuesta.num_buena_calificacion=respuesta.num_buena_calificacion+1
                respuesta.num_mala_calificacion=respuesta.num_mala_calificacion-1
                respuesta.save()
                califi.save()
         
        else:
            ahora = dt.now()
            fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")
            califi=usuarios.Calificacion(
                fecha_de_creacion=fecha,
                fecha_de_modificacion=fecha,
                estado=True,
                respuesta_id=cal,
                usuario_id=usuario.id                
            )
            califi.save()
            respuesta.num_buena_calificacion=respuesta.num_buena_calificacion+1
            respuesta.save() 
        
        sistemaDeNivel(request, respuesta)

        return HttpResponse('{"likes":'+str(respuesta.num_buena_calificacion)+',"dislikes":'+str(respuesta.num_mala_calificacion)+'}')

    elif request.GET.get("dislike",""):
        if usuarios.Calificacion.objects.filter(usuario_id=usuario.id,respuesta_id=cal).exists():
            
            califi=list(usuarios.Calificacion.objects.filter(usuario_id=usuario.id,respuesta_id=cal))[0]
            print(califi.estado)
            if (califi.estado == False):
                respuesta.num_mala_calificacion=respuesta.num_mala_calificacion-1
                respuesta.save()
                califi.delete()
            else:
                califi.estado = False
                respuesta.num_buena_calificacion=respuesta.num_buena_calificacion-1
                respuesta.num_mala_calificacion=respuesta.num_mala_calificacion+1
                respuesta.save()
                califi.save()
        
        else:
            ahora = dt.now()
            fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")
            califi=usuarios.Calificacion(
                fecha_de_creacion=fecha,
                fecha_de_modificacion=fecha,
                estado=False,
                respuesta_id=cal,
                usuario_id=usuario.id                
            )
            califi.save()
            respuesta.num_mala_calificacion=respuesta.num_mala_calificacion+1
            respuesta.save()
        
        sistemaDeNivel(request, respuesta)
                    
        return HttpResponse('{"likes":'+str(respuesta.num_buena_calificacion)+',"dislikes":'+str(respuesta.num_mala_calificacion)+'}')
    
    return HttpResponse('{"likes":'+str(respuesta.num_buena_calificacion)+',"dislikes":'+str(respuesta.num_mala_calificacion)+'}')

def sistemaDeNivel(request,respuesta):
    diferencia=respuesta.num_buena_calificacion - respuesta.num_mala_calificacion
    respuesta.aprobacion=diferencia
    respuesta.save()
    if (diferencia >= 20):
        if(respuesta.confiabilidad_id != 20):
            respuesta.confiabilidad_id=2
            #usuario de la respuesta
            u_d_l_r=usuarios.Usuario.objects.get(id=respuesta.usuario_id)
            temp=u_d_l_r.num_resp_confiables if u_d_l_r.num_resp_confiables else 0
            u_d_l_r.num_resp_confiables=temp+1
            respuesta.save()
            u_d_l_r.save()
            #verifica la cantidad de resp_confiables que tiene el usuario para subir de nivel
            if( 0<=u_d_l_r.num_resp_confiables and u_d_l_r.num_resp_confiables <=4 ):
                u_d_l_r.nivel_id=1
                u_d_l_r.save()
            elif ( 5<=u_d_l_r.num_resp_confiables and u_d_l_r.num_resp_confiables <=9 ):
                u_d_l_r.nivel_id=2
                u_d_l_r.save()
            elif ( 10<=u_d_l_r.num_resp_confiables and u_d_l_r.num_resp_confiables <=19 ):
                u_d_l_r.nivel_id=3
                u_d_l_r.save()
            elif ( 20<=u_d_l_r.num_resp_confiables):
                u_d_l_r.nivel_id=3
                u_d_l_r.save()
            else:
                u_d_l_r.nivel_id=1
                u_d_l_r.save()

    else:
        if(respuesta.confiabilidad_id != 19):
            respuesta.confiabilidad_id=1
            #usuario de la respuesta
            u_d_l_r=usuarios.Usuario.objects.get(id=respuesta.usuario_id)
            u_d_l_r.num_resp_confiables=(u_d_l_r.num_resp_confiables if u_d_l_r.num_resp_confiables else 1)-1
            respuesta.save()
            u_d_l_r.save()
            if( 0<=u_d_l_r.num_resp_confiables and u_d_l_r.num_resp_confiables <=4 ):
                u_d_l_r.nivel_id=1
                u_d_l_r.save()
            elif ( 5<=u_d_l_r.num_resp_confiables and u_d_l_r.num_resp_confiables <=9 ):
                u_d_l_r.nivel_id=2
                u_d_l_r.save()
            elif ( 10<=u_d_l_r.num_resp_confiables and u_d_l_r.num_resp_confiables <=19 ):
                u_d_l_r.nivel_id=3
                u_d_l_r.save()
            elif ( 20<=u_d_l_r.num_resp_confiables):
                u_d_l_r.nivel_id=3
                u_d_l_r.save()
            else:
                u_d_l_r.nivel_id=1
                u_d_l_r.save()
    return ""

#buscar
def search_e(request):
    indices = ["enunciado__icontains", "area_id", "tema_id", "fecha_de_modificacion__gte"]
    enunciado = request.GET.get("enum","")
    area = request.GET.get("id_ar","")
    tema = request.GET.get("id_tem","")
    fecha = request.GET.get("date","")
    objetos = [enunciado, area, tema, fecha]
    filtro = {}
    
    for i in range (4):
        if objetos[i] != "":
            filtro[indices[i]]=objetos[i]      
    preguntas=list(usuarios.Pregunta.objects.filter(**filtro))

    pregunta_usuario=[]
    for pregunta in preguntas:
        usuario=usuarios.Usuario.objects.get(id=pregunta.usuario_id)
        pregunta_usuario.append([pregunta,usuario])

    return render(request,"busqueda.html",{"preguntas":pregunta_usuario}) 

def aniadir_respuesta(request):
    usuario=request.GET.get("usuario","")
    pregunta_id=request.GET.get("pregunta_id","")
    contenido=request.GET.get("contenido","")
    ahora = dt.now()
    fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")
    usuario=usuarios.Usuario.objects.get(usuario=usuario)
    respuesta_nueva=usuarios.Respuesta(
        contenido=contenido,
        num_buena_calificacion=0,
        num_mala_calificacion=0,
        fecha_de_creacion=fecha,
        fecha_de_modificacion=fecha,
        estado=1,
        confiabilidad_id=1,
        pregunta_id=int(pregunta_id),
        usuario_id=usuario.id                
    )
    respuesta_nueva.save()
    return HttpResponse("se añadio respuesta "+str(usuario)+" "+str(usuario.id))

def eliminar_respuesta(request):
    respuesta_id=request.GET.get("respuesta_id","")
    resp_eliminada=usuarios.Respuesta.objects.get(id=respuesta_id).delete()
    return HttpResponse("se elimino")

def editar_respuesta(request):
    respuesta_id=request.GET.get("id","")
    contenido=request.GET.get("nuevoContenido","")
    ahora = dt.now()
    fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")
    respuesta=usuarios.Respuesta.objects.filter(id=int(respuesta_id)).update(contenido=contenido,fecha_de_modificacion=fecha)
    return HttpResponse("se cambio contenido")

#Aqui empiezan mis vistas (Jimy)

@login_required()
def verHistorial(request, id):
    if(id == request.user.id) :
        #otherFalseUser=usuarios.User.objects.get(id=id)
        #Importamos todos los usuarios, preguntas y respuestas
        falseUser=usuarios.Usuario.objects.get(usuario=request.user.username)

        allUsers=usuarios.Usuario.objects.all()
        allQuestions=usuarios.Pregunta.objects.all()
        allAnswers=usuarios.Respuesta.objects.all()
        print(falseUser.id)
        userQuestions=usuarios.Pregunta.objects.filter(usuario_id = falseUser.id)
        print("userQuestions")
        print(userQuestions)
        userAnswers=usuarios.Respuesta.objects.filter(usuario_id = falseUser.id)

        resFiltradas=usuarios.Respuesta.objects.filter(usuario_id=falseUser.id)
        #print(respuestasFiltradas)
        """
        for falAnswer in respuestasFiltradas :
            for someQuestion in allQuestions :
                if someQuestion.id == falAnswer.pregunta_id :
                    print(someQuestion.enunciado)
                    print(someQuestion.usuario)
                    print("Esta es una pregunta")"""


        """print(request.user.username)
        print(falseUser.usuario)
        print("Hasta aqui")"""
        #currUser=usuarios.Usuario.objects.get(usuario=request.user.username)
        #print(currUser.nombre)
        """
        currUser=auth.authenticate(username=currUser.usuario,password=currUser.contrasenia)
        auth.login(request,currUser)
        currUser=usuarios.Usuario.objects.get(id=id)"""
        return render(request, "verHistorial.html", {'resFiltradas': resFiltradas ,'currUser': falseUser, 'questions': userQuestions, 'answers': userAnswers ,'allQuestions' : allQuestions, 'allAnswers':allAnswers, 'users':allUsers })
    else:
        messages.info(request,'Usted no esta autorizado a ver este perfil o este perfil ya no existe')
        return redirect(reverse('foro'))

#esta ya esta
@login_required()
def editarPerfil(request, id):
    falseUser=usuarios.Usuario.objects.get(usuario=request.user.username)
    perfilPersona=usuarios.Usuario.objects.get(id=id)
    if(perfilPersona.usuario == request.user.username):
        if request.method=='POST':
            print("Se edita el usuario")
            editUser=usuarios.Usuario.objects.get(usuario=request.user.username)
            editUser.nombre=request.POST['nombre']
            editUser.contrasenia=request.POST['contrasenia']
            editUser.celular=request.POST['celular']
            #Comprobacion numero de Celular
            if request.POST['celular'] == "" :
                print("no puso  o se quito numero de telefono")
                editUser.celular=None
                editUser.save()
            else:
                editUser.Celular=request.POST['celular']
            #Comprabacion fecha de nacimiento
            if request.POST['nacimiento'] == "" :
                print("la fecha esta vacia")
            else:
                editUser.fecha_de_nacimiento=request.POST['nacimiento']
            """try :
                editUser.fecha_de_nacimiento=request.POST['nacimiento']
            except:
                editUser.fecha_de_nacimiento=date(2020,1,1)"""
            hoy=dt.now()
            print(hoy.day)
            print(hoy.month)
            print(hoy.year)
            #editUser.fecha_de_modificacion=hoy.strftime('%d-%m-%Y') #- datetime.date.today
            #editUser.fecha_de_modificacion=dt.date.today()
            editUser.fecha_de_modificacion=dt.now()
            editUser.save()
            messages.info(request,'Se guardaron los cambios')
            return redirect(reverse('foro'))
        else:
            currUser=usuarios.Usuario.objects.get(usuario=request.user.username)
            if(currUser.fecha_de_nacimiento == None):
                return render(request,"editarPerfil.html",{'currUser':currUser})
            else:
                print(currUser.fecha_de_nacimiento)
                fechaCumpleanios=dt(currUser.fecha_de_nacimiento.year, currUser.fecha_de_nacimiento.month, currUser.fecha_de_nacimiento.day)
            #print(fechaCumpleanios)
            return render(request,"editarPerfil.html",{'currUser':currUser, 'fechaCumpleanios':fechaCumpleanios})
    else:
        messages.info(request,'Usted no esta autorizado a editar este perfil o este perfil no existe')
        return redirect(reverse('foro'))

@login_required
def eliminarCuenta(request, id):
    if request.method=='POST':
        #print(request.user.nombre)
        delUser=usuarios.Usuario.objects.get(usuario=request.user.username)
        if(request.POST['nomUsuario'] == delUser.usuario ):
            delUser.delete()
            delAuth=request.user
            delAuth.delete()
            logout(request)
            messages.info(request,'Se elimino la cuenta')
            return redirect(reverse('foro'))
        else:
            messages.info(request,'No se pudo eliminar la cuenta')
            return redirect(reverse('foro'))
    else:
        return redirect(reverse('foro'))

@login_required
def eliminarPregunta(request, id):
    selQuestion=usuarios.Pregunta.objects.get(id=id)
    currUser=usuarios.Usuario.objects.get(usuario=request.user.username)
    if(selQuestion.usuario_id == currUser.id) :
        selQuestion.delete()
        print("Se elimino la pregunta")
        messages.info(request,'Eliminaste la pregunta')
        return redirect(reverse('foro'))
    else:
        messages.info(request,'No se elimino la pregunta porque tu no la creaste o la pregunta no existe')
        return redirect(reverse('foro'))

@login_required
def eliminarRespuesta(request, id):
    selAnswer=usuarios.Respuesta.objects.get(id=id)
    if(selAnswer.usuario_id == request.user.id) :
        selAnswer.delete()
        print("Se elimino la respuesta")
        messages.info(request,'Eliminaste la respuesta')
        return redirect(reverse('foro'))
    else:
        messages.info(request,'No se elimino la resspuesta porque tu no la creaste o la pregunta no existe')
        return redirect(reverse('foro'))
#Fin de mis vistas

#agregarpregunta
@login_required()
def formular_p(request):
    temas = list(usuarios.Tema.objects.all())
    areas = list(usuarios.Area.objects.all())
    return render(request, 'formular_p.html',{"temas":temas,"areas":areas})
    
def Enviar_Pregunta(request):
    print(request.GET)
    d_usuario=usuarios.Usuario.objects.get(usuario=request.GET.get("usuario","")).id
    d_enunciado = request.GET.get("enun","")
    d_area = request.GET.get("id_ar","")
    d_tema = request.GET.get("id_tem","")
    d_descripcion = request.GET.get("descrip","")
    
    ahora = dt.now()
    fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")
    #usuario=usuarios.Usuario.objects.get(usuario=usuario)
    pregunta_nueva=usuarios.Pregunta(
        enunciado=d_enunciado,
        area_id=d_area,
        tema_id=d_tema,
        descripcion=d_descripcion,
        fecha_de_creacion=fecha,
        fecha_de_modificacion=fecha,
        estado=1,
        usuario_id=d_usuario           
    )
    print(pregunta_nueva.usuario_id)
    pregunta_nueva.save()
    preguntas = list(usuarios.Pregunta.objects.all())
    #return render(request, 'foro.html',{"preguntas":preguntas})   
    return redirect('../foro/',{"preguntas":preguntas})  


def aniadir_comentario_a_respuesta(request):
    usuario_id=usuarios.Usuario.objects.get(usuario=request.GET.get("usuario","")).id
    ahora = dt.now()
    fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")
    comentarioNuevo=usuarios.Comentario(
        contenido=request.GET.get("nuevoComentario",""),
        fecha_de_creacion=fecha,
        fecha_de_modificacion=fecha,
        estado=1,
        respuesta_id=int(request.GET.get("id","")),
        usuario_id=usuario_id,
    )
    comentarioNuevo.save()
    return HttpResponse("exito")

def aniadir_comentario_a_comentario(request):
    respuesta_id=usuarios.Comentario.objects.get(id=int(request.GET.get("id",""))).respuesta_id
    usuario_id=usuarios.Usuario.objects.get(usuario=request.GET.get("usuario","")).id
    ahora = dt.now()
    fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")
    comentarioNuevo=usuarios.Comentario(
        contenido=request.GET.get("nuevoSubComentario",""),
        comentario_id=int(request.GET.get("id","")),
        fecha_de_creacion=fecha,
        fecha_de_modificacion=fecha,
        estado=1,
        respuesta_id=respuesta_id,
        usuario_id=usuario_id,
    )
    comentarioNuevo.save()
    return HttpResponse("exito")

def eliminar_comentario(request):
    comentario_id=request.GET.get("comentario_id","")
    sub_com=usuarios.Comentario.objects.filter(comentario_id=comentario_id).delete()
    com_eliminada=usuarios.Comentario.objects.get(id=comentario_id).delete()
    return HttpResponse("Se elimino")


def editar_comentario(request):
    comentario_id=request.GET.get("id","")
    contenido=request.GET.get("nuevoContenido","")
    ahora = dt.now()
    fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")
    respuesta=usuarios.Comentario.objects.filter(id=int(comentario_id)).update(contenido=contenido,fecha_de_modificacion=fecha)
    return HttpResponse("Exito")

def eliminar_pregunta(request):
    pregunta_id=request.GET.get("pregunta_id","")
    pregunta_eliminada=usuarios.Pregunta.objects.get(id=pregunta_id).delete()
    return HttpResponse(pregunta_id)

def informacion_Usuario(request):
    if not (request.GET.get("usuario","")):
        return HttpResponse("Usuario no encontrado")
    elif not (usuarios.Usuario.objects.filter(id=request.GET.get("usuario","")).exists()):
        return HttpResponse("Usuario no encontrado")

    usuario=usuarios.Usuario.objects.get(id=request.GET.get("usuario",""))
    respuestas=list(usuarios.Respuesta.objects.filter(usuario_id=request.GET.get("usuario",""),confiabilidad_id=2))
    preguntas=[]
    for respuesta in respuestas:
        preguntas.append(usuarios.Pregunta.objects.get(id=respuesta.pregunta_id))
    
    if usuarios.Nivel.objects.filter(id=usuario.nivel_id).exists():
        nivel=usuarios.Nivel.objects.get(id=usuario.nivel_id)
    else:
        nivel = "Basico"
    return render(request,"usuario.html",{"usuario":usuario,"respuestas":respuestas,"preguntas":preguntas,"nivel":nivel})