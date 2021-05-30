from . import views
from django.urls import path, include
 
urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path('register/', views.register, name='register'),
    path('room/', views.register_room, name='register_room'),
    path('', views.index, name='index'),
    path('<int:chat_room_id>', views.index, name='chat_room'),
]