from django.contrib.auth.models import User  # 新增这行，导入User模型
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeResponseSerializer
from notifications.models import Notification
from .pagination import StandardResultsSetPagination
from rest_framework import permissions
from django.db.models import F
from notifications.models import Notification


class PostListView(generics.ListAPIView):
    """获取动态列表接口"""
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination  # 启用分页
    permission_classes = []  # 新增：文档要求公开访问，不加权限

    def get_queryset(self):
        return Post.objects.all().order_by('-created_time')  # 保持不变（你的模型字段是created_time，没问题）

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            # 修改前：return self.get_paginated_response({...}) （带count/next，不符合文档）
            return Response({  # 修改后：按文档格式封装
                'success': True,
                'data': {
                    'posts': serializer.data,
                    'total': queryset.count()
                }
            })

        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response({
            'success': True,
            'data': {
                'posts': serializer.data,
                'total': queryset.count()
            }
        })


class LikePostView(generics.CreateAPIView):
    """点赞/取消点赞接口"""
    permission_classes = [IsAuthenticated]  
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({'success': False, 'message': '动态不存在'}, status=status.HTTP_404_NOT_FOUND)

        # 修改：删除冗余的admin_user查询（request.user就是当前登录用户，无需单独查）
        admin_user = request.user

        liked = request.data.get('liked', False)
        like_exists = Like.objects.filter(post=post, user=admin_user).exists()

        if liked:
            if not like_exists:
                Like.objects.create(post=post, user=admin_user)
                post.likes += 1
        else:
            if like_exists:
                Like.objects.filter(post=post, user=admin_user).delete()
                post.likes = max(0, post.likes - 1)

        post.save()
        # 修改：删除冗余的serializer = self.get_serializer(post)（响应里没用）

        return Response({
            'success': True,
            'message': '操作成功',
            'data': {'likes': post.likes}
        }, status=status.HTTP_200_OK)


class CommentListCreateView(generics.ListCreateAPIView):
    """合并：获取评论列表（GET）+ 发布评论（POST）"""
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    # 控制权限：GET公开，POST需登录
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return []

    # 获取指定动态的评论列表（GET逻辑）
    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        return Comment.objects.filter(post_id=post_id).order_by('-created_time')

    # 发布评论的逻辑（POST逻辑）
    def perform_create(self, serializer):
        post_id = self.kwargs.get('pk')
        post = Post.objects.get(pk=post_id)
        # 保存评论（关联当前用户和动态）
        serializer.save(user=self.request.user, post=post)
        # 更新动态评论数
        post.comments = F('comments') + 1
        post.save()
        post.refresh_from_db()
        # 创建通知
        Notification.objects.create(
            user=post.user,
            from_user=self.request.user,
            post=post,
            type='comment'
        )

    # 重写list方法，匹配文档格式
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({
                'success': True,
                'data': {
                    'comments': serializer.data,
                    'total': queryset.count()
                }
            })
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': {
                'comments': serializer.data,
                'total': queryset.count()
            }
        })