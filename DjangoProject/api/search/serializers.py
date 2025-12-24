####################  搜索部分开始  ######################
from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models import Post
from .models import SearchHistory

User = get_user_model()

# --------------- 1.Post  ---------------
class PostSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'name', 'avatar', 'time', 'text', 'type', 'media',
                  'likes', 'comments', 'liked']

    def get_avatar(self, obj):
        profile = getattr(obj.user, 'profile', None)
        if profile and profile.avatar:
            return profile.avatar
        return 'https://picsum.photos/200'

    def get_time(self, obj):
        from django.utils.timesince import timesince
        return timesince(obj.created_at, locale='zh_CN') + '前'

    def get_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False

    def get_likes(self, obj):
        return obj.likes_count

    def get_comments(self, obj):
        return obj.comments_count

# --------------- 2.搜索历史  ---------------
class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ['keyword','tag','date']
####################  搜索部分结束  ######################