from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils import timezone

from apps.detection.models import DetectionEvent
from apps.detection.constants import _CRITICAL_CLASSES, _VIOLATION_LABEL

def unauthorized(request):
    return render(request, 'error/required.html')

@login_required(login_url=reverse_lazy('unauthorized'))
def home(request):
    today = timezone.now().date()

    all_today = DetectionEvent.objects.filter(timestamp__date=today)
    violations_today = all_today.filter(class_name__startswith='Sem')

    violations_count = violations_today.count()
    total_count = all_today.count()
    compliance_rate = round((1 - violations_count / total_count) * 100, 1) if total_count else 100.0
    critical_count = violations_today.filter(class_name__in=_CRITICAL_CLASSES).count()

    recent_events = []
    for ev in violations_today.order_by('-timestamp')[:5]:
        is_critical = ev.class_name in _CRITICAL_CLASSES
        recent_events.append({
            'time': timezone.localtime(ev.timestamp).strftime('%H:%M'),
            'violation': _VIOLATION_LABEL.get(ev.class_name, ev.class_name),
            'camera': ev.camera_id or 'CAM-01',
            'badge': 'badge-danger' if is_critical else 'badge-warning',
            'severity': 'Critical' if is_critical else 'Warning',
        })

    return render(request, 'home/home.html', {
        'compliance_rate': compliance_rate,
        'violations_count': violations_count,
        'critical_count': critical_count,
        'recent_events': recent_events,
    })

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
