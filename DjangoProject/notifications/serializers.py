from rest_framework import serializers
from .models import Notification
from posts.models import Post
from datetime import datetime



class NotificationSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='from_user.username')
    avatar = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    # 新增：匹配文档的postId字段（原post字段改成postId）
    postId = serializers.IntegerField(source='post.id', read_only=True)
    # 文档要求的postText（动态内容）
    postText = serializers.ReadOnlyField(source='post.text')

    class Meta:
        model = Notification
        # 匹配文档的通知响应字段
        fields = ['id', 'type', 'name', 'avatar', 'time', 'read', 'postId', 'postText']

    def get_avatar(self, obj):
        return f"https://picsum.photos/200?{obj.from_user.id}"

    def get_time(self, obj):
        now = datetime.now()
        diff = now - obj.created_time.replace(tzinfo=None)
        if diff.seconds < 60:
            return "刚刚"
        elif diff.seconds < 3600:
            return f"{diff.seconds//60}分钟前"
        elif diff.days < 1:
            return f"{diff.seconds//3600}小时前"
        else:
            return f"{diff.days}天前"