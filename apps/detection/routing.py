from django.urls import path
from ..myapp import consumers

websocket_urlpatterns = [
    path('ws/video_feed/', consumers.VideoFeedConsumer.as_asgi()),
]
