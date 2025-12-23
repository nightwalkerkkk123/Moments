from rest_framework import serializers
from .models import Notification
from datetime import datetime


class NotificationSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='actor.username')
    avatar = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    # 匹配文档的postId字段（使用content_object获取post id）
    postId = serializers.SerializerMethodField()
    # 文档要求的postText（动态内容）
    postText = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        # 匹配文档的通知响应字段
        fields = ['id', 'type', 'name', 'avatar', 'time', 'is_read', 'postId', 'postText']

    def get_avatar(self, obj):
        return f"https://picsum.photos/200?{obj.actor.id}"

    def get_time(self, obj):
        now = datetime.now()
        diff = now - obj.created_at.replace(tzinfo=None)
        if diff.seconds < 60:
            return "刚刚"
        elif diff.seconds < 3600:
            return f"{diff.seconds//60}分钟前"
        elif diff.days < 1:
            return f"{diff.seconds//3600}小时前"
        else:
            return f"{diff.days}天前"

    def get_postId(self, obj):
        # 从content_object获取post id
        if hasattr(obj.content_object, 'id'):
            return obj.content_object.id
        return None

    def get_postText(self, obj):
        # 从content_object获取post文本
        if hasattr(obj.content_object, 'text'):
            return obj.content_object.text
        return None
