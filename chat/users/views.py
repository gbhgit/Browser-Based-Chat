from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import CustomUserCreationForm
from .forms import ChatRoomForm
from .serializers import PostListSerializer
from .models import ChatRoom, Post
from django.contrib.auth.decorators import login_required
from django.views import generic
from rest_framework.decorators import api_view
from django.http import JsonResponse

@login_required
@api_view(['POST'])
def get_all_room_posts(request):
    room_id = request.POST['room_id']
    room = ChatRoom.objects.get(pk=room_id)
    num_results = ChatRoom.objects.filter(pk=room_id).count()
    if num_results < 1:
        return JsonResponse({'posts': None})
    elif len(Post.objects.filter(room=room)) > 50:
        posts = Post.objects.filter(room=room).order_by('-created')[: 50]
    else:
        posts = Post.objects.filter(room=room).order_by('-created')
        
    for post in posts:
        post.creator = post.created_by.username
        post.created_date = post.created.strftime('%Y-%m-%d')
        post.created_time = post.created.strftime('%H:%M')
    response = {'posts': PostListSerializer(posts, many=True).data,}

    return JsonResponse(response)

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