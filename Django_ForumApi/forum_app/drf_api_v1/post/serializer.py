from rest_framework import serializers
from forum_app.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content']

class ReadPostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'username', 'date_created', 'content']
    def get_username(self, obj):
        return obj.writer.user.username
