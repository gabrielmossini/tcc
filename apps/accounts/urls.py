from django.urls import path
#from django.shortcuts import render
from . import views

urlpatterns = [
    path('unauthorized', views.unauthorized, name='unauthorized'),
    path('', views.login, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('login/create/', views.create, name='create_user'),
    #path('store/', views.store, name='store'),
    path('view/', views.view, name='view_users'),
    path('user/<int:user_id>/', views.view_user, name='view_user'),
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('user/<int:user_id>/update/', views.update_user, name='update_user'),
    path('users-pdf/', views.users_PDF, name='users_PDF'), 
]
