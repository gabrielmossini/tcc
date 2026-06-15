from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


def unauthorized(request):
    return render(request, 'error/required.html')


@login_required(login_url=reverse_lazy('unauthorized'))
def home(request):
    return render(request, 'home/home.html')


def about(request):
    return render(request, 'about/about.html')


def custom_404_view(request, exception):
    return render(request, 'error/404.html', status=404)


def custom_403_view(request, exception):
    return render(request, 'error/403.html', status=403)


def login(request):
    data = {}
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                data['mensagem'] = 'Usuário ou Senha Inválidos!!'
                data['class'] = 'alert-danger'
        else:
            data['mensagem'] = 'Por favor, preencha todos os campos.'
            data['class'] = 'alert-warning'

    return render(request, 'accounts/login.html', data)


def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')
