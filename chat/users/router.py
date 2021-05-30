from django.urls import path
from . import ws

websocket_urlpatterns = [
    path('ws/<str:room_id>/', ws.Consumer.as_asgi()),
]