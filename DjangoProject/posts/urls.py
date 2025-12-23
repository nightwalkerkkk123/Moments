from django.urls import path
from .views import (
    PostListView,
    LikePostView,
    CommentListCreateView  # 合并后的评论视图
)

urlpatterns = [
    # 获取动态列表
    path('', PostListView.as_view(), name='post-list'),
    # 点赞接口
    path('<int:pk>/like/', LikePostView.as_view(), name='post-like'),
    # 评论接口（GET/POST）
    path('<int:pk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
]