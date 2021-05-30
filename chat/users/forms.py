from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from django.forms import ModelForm
from .models import ChatRoom

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

class ChatRoomForm(ModelForm):
    class Meta:
        model = ChatRoom
        fields = ("room_name",)