from django.urls import path
from . import views

urlpatterns = [
    path('toggle-mute/', views.toggle_mute, name='toggle_mute'),
    path('detect/', views.detect, name='detect'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('get_detections/', views.get_detections, name='get_detections'),    
]
