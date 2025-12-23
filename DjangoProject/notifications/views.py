from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
from posts.pagination import StandardResultsSetPagination
from rest_framework import serializers  # 新增：导入空Serializer


# class NotificationListView(generics.ListAPIView):
#     """获取消息通知列表"""
#     permission_classes = [IsAuthenticated]
#     serializer_class = NotificationSerializer
#     pagination_class = StandardResultsSetPagination

#     def get_queryset(self):
#         return Notification.objects.filter(user=self.request.user).order_by('-created_time')

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response({
#                 'success': True,
#                 'data': {
#                     'notifications': serializer.data,
#                     'total': queryset.count()
#                 }
#             })

#         serializer = self.get_serializer(queryset, many=True)
#         return Response({
#             'success': True,
#             'data': {
#                 'notifications': serializer.data,
#                 'total': queryset.count()
#             }
#         })

class NotificationListView(generics.ListAPIView):
    """获取消息通知列表"""
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_time')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        # 新增：统计未读通知数量（文档备注强制要求）
        total_unread = queryset.filter(read=False).count()

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # 修改前：return self.get_paginated_response({...}) （格式不符合文档）
            return Response({  # 修改后：按文档格式封装，去掉count/next/previous
                'success': True,
                'data': {
                    'notifications': serializer.data,
                    'total': queryset.count(),
                    'total_unread': total_unread  # 新增未读数量字段
                }
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': {
                'notifications': serializer.data,
                'total': queryset.count(),
                'total_unread': total_unread  # 新增未读数量字段
            }
        })


# class MarkAsReadView(generics.CreateAPIView):
#     """标记通知为已读"""
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         notification_ids = request.data.get('notificationIds', [])
#         if notification_ids:
#             Notification.objects.filter(
#                 id__in=notification_ids,
#                 user=request.user
#             ).update(read=True)
#         else:
#             # 为空时标记全部
#             Notification.objects.filter(user=request.user).update(read=True)

#         return Response({
#             'success': True,
#             'message': '操作成功'
#         })

class MarkAsReadView(generics.CreateAPIView):
    """标记通知为已读（支持单条/全部，文档要求）"""
    permission_classes = [IsAuthenticated]
    # 新增：按DRF规范补充空Serializer（避免潜在警告，不影响功能）
    serializer_class = serializers.Serializer

    def create(self, request, *args, **kwargs):
        notification_ids = request.data.get('notificationIds', [])
        user = request.user

        if notification_ids:
            # 标记指定ID的通知为已读（仅更新未读的）
            Notification.objects.filter(
                id__in=notification_ids,
                user=user,
                read=False  # 优化：只更新未读的，避免重复操作
            ).update(read=True)
        else:
            # 标记全部已读（仅更新未读的，效率更高）
            Notification.objects.filter(user=user, read=False).update(read=True)

        # 响应格式已符合文档，无需修改
        return Response({
            'success': True,
            'message': '操作成功'
        })