from django.urls import path
from . import views

urlpatterns = [
    path('unauthorized', views.unauthorized, name='unauthorized'),
    path('', views.login, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
]
