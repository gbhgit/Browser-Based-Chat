from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import CustomUserCreationForm
from .forms import ChatRoomForm
from .models import ChatRoom
from django.contrib.auth.decorators import login_required
from django.views import generic

@login_required
def index(request, chat_room_id=None):
    if chat_room_id != None:
        num_results = ChatRoom.objects.filter(id = chat_room_id).count()
        if num_results > 0:
            room = ChatRoom.objects.get(id = chat_room_id)
            room.room_users.add(request.user)
            context = {'room': room,}
            return render(request, "chat/chat.html", context)
        else:
            rooms = ChatRoom.objects.all()
            context = {'rooms': rooms,}
            return render(request, "users/home.html", context)
    else:
        rooms = ChatRoom.objects.all()
        context = {'rooms': rooms,}
        return render(request, "users/home.html", context)

@login_required
def register_room(request):
    form = ChatRoomForm()
    if request.method == 'POST':
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("index"))
    context = {'form': form}
    return render(request, "room/register.html", context)

def register(request):
    if request.method == "GET":
        return render(request, "users/register.html", {"form": CustomUserCreationForm})
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("index"))