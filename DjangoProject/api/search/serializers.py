####################  搜索部分开始  ######################
from rest_framework import serializers
from .models import Post, SearchHistory   # 现在从当前包引
# --------------- 1.Post  ---------------
class PostSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='author.username', read_only=True)
    avatar = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    # 尝试实时更新评论数
    comments = serializers.IntegerField(source='comment_set.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id','name','avatar','time','text','type','media',
                  'tag','likes','comments','liked']

    def get_avatar(self, obj):
        # 用户头像字段，如无则返回默认
        return getattr(obj.author, 'avatar', 'https://picsum.photos/200')

    def get_time(self, obj):
        # 友好时间
        from django.utils.timesince import timesince
        return timesince(obj.created_at, locale='zh_CN') + '前'

    def get_liked(self, obj):
        # 当前登录用户是否点过赞（需传request上下文）
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.like_set.filter(user=user).exists()
        return False

# --------------- 2.搜索历史  ---------------
class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ['keyword','tag','date']
####################  搜索部分结束  ######################