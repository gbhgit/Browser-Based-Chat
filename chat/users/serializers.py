from .models import ChatRoom, Post
from rest_framework import serializers

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'

class PostListSerializer(serializers.Serializer):
    msn = serializers.CharField()
    created_by = serializers.CharField()
    created_date = serializers.CharField()
    created_time = serializers.CharField()