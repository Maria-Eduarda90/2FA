from django.shortcuts import render
from django.http import HttpResponse
from .utils import password_is_valid, send_email
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth
from django.conf import settings
import os

def register(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'register.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not password_is_valid(request, password, confirm_password):
            return redirect('/auth/register')

        try:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            is_active=False)
            user.save()
            path_template = os.path.join(settings.BASE_DIR, 'base/templates/emails/register_confirm.html')
            send_email(path_template, 'Cadastro confirmado', [email,], username=username)
            messages.add_message(request, constants.SUCCESS, 'Usuario criado com sucesso')
            return redirect('/auth/login')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/auth/register')


def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')
    elif request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        if not user:
            messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
            return redirect('/auth/login')
        else:
            auth.login(request, user)
            return redirect('/')

def logout(request):
    auth.logout(request)
    return redirect('/auth/register')