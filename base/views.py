from django.shortcuts import render
from django.http import HttpResponse
from .utils import password_is_valid, send_email
from django.shortcuts import redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth
from django.conf import settings
import os
from .models import Activation
from hashlib import sha256

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

            token = sha256(f"{username}{email}".encode()).hexdigest()
            activation = Activation(token=token, user=user)
            activation.save()
            
            path_template = os.path.join(settings.BASE_DIR, 'base/templates/emails/register_confirm.html')
            send_email(path_template, 'Cadastro confirmado', [email,], username=username, link_activation=f"127.0.0.1:8000/auth/activate_account/{token}")

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
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if not user:
            messages.add_message(request, constants.INFO, 'Verifique seu email para poder ativar a sua conta')
            return redirect('/auth/login')
        else:
            auth.login(request, user)
            return redirect('/')

def logout(request):
    auth.logout(request)
    return redirect('/auth/login')

def activate_account(request, token):
    token = get_object_or_404(Activation, token=token)
    if token.active:
        messages.add_message(request, constants.WARNING, 'Esse token já foi usado')
        return redirect('/auth/login')

    user = User.objects.get(username=token.user.username)
    user.is_active = True
    user.save()

    token.active = True
    token.save()

    messages.add_message(request, constants.SUCCESS, 'Conta ativa com sucesso')
    return redirect('/auth/login')