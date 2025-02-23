#from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.models import User
from django.db import connection, transaction
from django.contrib import messages
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from .models import Profile
from .forms import UserForm, ProfileForm

def unauthorized(request):
    return render(request, 'error/required.html')

@login_required(login_url=reverse_lazy('unauthorized'))
def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'about/about.html')

def privacy(request):
    return render(request, 'about/privacy.html')

def terms(request):
    return render(request, 'about/terms.html')

def custom_404_view(request, exception):
    return render(request, 'error/404.html', status=404)

def custom_403_view(request, exception):
    return render(request, 'error/403.html', status=403)

@login_required(login_url=reverse_lazy('unauthorized'))
def create(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid:
            with transaction.atomic():
                user = user_form.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
            messages.success(request, 'Usuário salvo com sucesso.')
            return redirect(f"{reverse('view_users')}?message=Usuário salvo com sucesso.")
        else:
            messages.error(request, 'Cadastro fracassou.')
            return redirect(f"{reverse('view_users')}?message=Cadastro Fracassou.")
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'login/create.html', {'user_form': user_form, 'profile_form': profile_form,})

def login(request):
    data = {}
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            print(f"User ID: {user.id}, Username: {user.username}")

            if user is not None:
                auth_login(request, user)   
                return redirect('home')
            else:
                data['mensagem'] = 'Usuário ou Senha Inválidos!!'
                data['class'] = 'alert-danger'
        else:
            data['mensagem'] = 'Por favor, preencha todos os campos.'
            data['class'] = 'alert-warning'

    return render(request, 'login/login.html', data)

def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

def calculate_age(birth_date):
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

@login_required(login_url=reverse_lazy('unauthorized'))
def view(request):
    users = User.objects.all().order_by('id')
    users = User.objects.select_related('profile').all()

    contex = {
        'users': users
    }
    
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'login/view.html', {'users': users, 'page_obj': page_obj})

@login_required(login_url=reverse_lazy('unauthorized'))
def view_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'login/view_user.html', {'user': user})

@login_required(login_url=reverse_lazy('unauthorized'))
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)

    print(f"User ID: {user.id}, Username: {user.username}")  # Debugging
    print(f"Profile Name: {profile.name}")  # Debugging

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user = user_form.save()
                profile_form.save()
            messages.success(request, 'Usuário atualizado com sucesso.')
            return redirect(f"{reverse('view_users')}?message=Usuário+atualizado+com+sucesso")
        else:
            messages.error(request, 'Erro ao atualizar o usuário.')  
            return redirect(f"{reverse('view_users')}?message=Erro+ao+atualizar+usuário")
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)
    
    return render(request, 'login/update.html', {'user_form': user_form, 'profile_form': profile_form, 'user': user, 'user_id': user_id})

@login_required(login_url=reverse_lazy('unauthorized'))
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuário deletado com sucesso.')
        return redirect(f"{reverse('view_users')}?message=Usuário+excluído+com+sucesso")
        #return redirect('view_users')
    return render(request, 'login/delete.html', {'user': user})

@login_required(login_url=reverse_lazy('unauthorized'))
def users_PDF(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="usuarios_relatorio.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, height - 50, "Todos os Usuários")

    pdf.setFont("Helvetica", 12)

    y = height - 80
    margin = 30

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                u.username,
                p.name,
                u.email,
                p.cpf,
                p.birthday,
                u.date_joined,
                u.is_active
            FROM
                auth_user u
            INNER JOIN
                myapp_profile p
            ON
                u.id = p.user_id
        """)
        users = cursor.fetchall()

        pdf.drawString(margin, y - 160, "-------------------------------------------------------")

        for item in users:
            if y < margin + 50:
                pdf.showPage()
                pdf.setFont("Helvetica-Bold", 14)
                pdf.drawString(100, height - 50, "Todos os Usuários:")
                pdf.setFont("Helvetica", 10)
                y = height - 80

            pdf.drawString(margin, y - 20, f"Nome: {item[1]}")
            pdf.drawString(margin, y - 40, f"Usuario: {item[0]}")
            pdf.drawString(margin, y - 60, f"Email: {item[2]}")
            pdf.drawString(margin, y - 80, f"CPF: {item[3]}")
            pdf.drawString(margin, y - 100, f"Data de Nascimento: {item[4]}")
            pdf.drawString(margin, y - 120, f"Data de Cadastro: {item[5]}")
            pdf.drawString(margin, y - 140, f"Status: {'Ativo' if item[6] else 'Inativo'}")
            y -= 180

    pdf.showPage()
    pdf.save()

    return response
