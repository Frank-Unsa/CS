from django.http import HttpResponse
from django.shortcuts import render, redirect
#Clases importadas para el login
from django.contrib import messages
from validate_email import validate_email
from usuarios import models as usuarios
from datetime import datetime as dt
from django. contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .decorators import auth_user_should_not_access
from django.contrib.auth.models import User


def hola(request):
    return HttpResponse("Hola mundo")

# Funciones de Internacionalizacion
def index(request):
    return render(request, "index.html",{})
def index2(request):
    return render(request, "index.html")
def about_us(request):
    return render(request, "about.html",)
    
def contact_us(request):
    return render(request, "contact.html",)

def pregunta_frecuente(request):
    return render(request, "frecuente.html",)
#Nuevo Registro 
@auth_user_should_not_access
def register(request):
    if request.method == 'POST':
        context = {'has_error': False, 'data': request.POST}
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        #Validacion de la longitud de la contrasenia
        if len(password) < 6:
            messages.add_message(request, messages.ERROR, 
            'El tamaño de la contraseña debe ser mayor a 6 caracteres')
            context['has_error'] = True
        #Validacion de las contrasenias iguales
        if password != password2:
            messages.add_message(request, messages.ERROR, 
            'Las contraseñas no coinciden')
            context['has_error'] = True
        #Validacion del correo electronico
        if not validate_email(email):
            messages.add_message(request, messages.ERROR, 
            'Ingrese un correo electrónico válido')
            context['has_error'] = True
        if not username:
            messages.add_message(request, messages.ERROR, 
            'El nombre de usuario es requerido')
            context['has_error'] = True
        #Validaciones si ya existe el nombre de usuario o 
        #el correo electronico
        if usuarios.Usuario.objects.filter(usuario=username).exists():
            messages.add_message(request, messages.ERROR, 
            'El nombre de usuario ya existe')
            context['has_error'] = True
        if usuarios.Usuario.objects.filter(correo=email).exists():
            messages.add_message(request, messages.ERROR, 
            'El correo electrónico ya existe')
            context['has_error'] = True

        #Si existe algun error se redirecciona nuevamente al registro
        if context['has_error']:
            return render(request, 'register.html', context)

        #Se obtiene la fecha y hora actual
        ahora = dt.now()
        fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")

        user = usuarios.Usuario(
                usuario = username,
                correo = email,
                contrasenia = password,
                fecha_de_creacion = fecha,
                fecha_de_modificacion = fecha,
                #faltaria el nivel
                nivel_id=1,
                num_resp_confiables=0,
                estado=True)
        user.save()
        #Se guarda tambien en la tabla auth_user
        user2 = User.objects.create_user(username=username, email=email)
        user2.set_password(password)
        user2.save()

        messages.add_message(request, messages.SUCCESS, 
            'La cuenta ha sido creada, ya puede iniciar sesion')
        return redirect('login')
    return render(request, 'register.html')

#Nuevo Login
#se cambia a login_user para distinguirlo del login importado
@auth_user_should_not_access
def login_user(request):
    if request.method == 'POST':
        context = {'data': request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.add_message(request,messages.ERROR,'Datos erróneos')
            return render(request, 'login.html', context)
        #retornar a la misma pagina luego de hacer el login
        login(request, user)
        messages.add_message(request,messages.SUCCESS,f'Bienvenido {user.username}')
        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        else:
            return redirect(reverse('foro'))

    return render(request, 'login.html')

#Nuevo logout
def logout_user(request):
    logout(request)
    messages.add_message(request,messages.SUCCESS,f'Se cerró la sesión correctamente')
    #Podria redigir al login 
    return redirect(reverse('foro'))
