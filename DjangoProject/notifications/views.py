from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer


# 自定义分页类（与其他应用保持一致）
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'pageSize'
    max_page_size = 100


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    """获取当前用户的通知列表"""
    # 获取通知列表，按时间倒序
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # 应用分页
    paginator = StandardResultsSetPagination()
    paginated_notifications = paginator.paginate_queryset(notifications, request)
    
    # 序列化
    serializer = NotificationSerializer(paginated_notifications, many=True, context={'request': request})
    
    # 统计未读通知数量
    total_unread = notifications.filter(is_read=False).count()
    
    return Response({
        'success': True,
        'data': {
            'notifications': serializer.data,
            'total': notifications.count(),
            'total_unread': total_unread  # 保持与文档一致的字段名
        }
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    """标记单个通知为已读"""
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        
        return Response({
            'success': True,
            'message': '操作成功'
        })
    except Notification.DoesNotExist:
        return Response({
            'success': False,
            'message': '通知不存在或无权操作'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def mark_all_notifications_read(request):
    """标记所有通知为已读"""
    # 更新当前用户的所有未读通知
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    return Response({
        'success': True,
        'message': '操作成功'
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_notification(request, notification_id):
    """删除单个通知"""
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.delete()
        
        return Response({
            'success': True,
            'message': '操作成功'
        })
    except Notification.DoesNotExist:
        return Response({
            'success': False,
            'message': '通知不存在或无权操作'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_all_notifications(request):
    """删除所有通知"""
    # 删除当前用户的所有通知
    Notification.objects.filter(user=request.user).delete()
    
    return Response({
        'success': True,
        'message': '操作成功'
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_as_read(request):
    """标记通知为已读（支持单条/全部，文档要求的旧接口）"""
    notification_ids = request.data.get('notificationIds', [])
    user = request.user

    if notification_ids:
        # 标记指定ID的通知为已读（仅更新未读的）
        Notification.objects.filter(
            id__in=notification_ids,
            user=user,
            is_read=False  # 优化：只更新未读的，避免重复操作
        ).update(is_read=True)
    else:
        # 标记全部已读（仅更新未读的，效率更高）
        Notification.objects.filter(user=user, is_read=False).update(is_read=True)

    # 响应格式已符合文档
    return Response({
        'success': True,
        'message': '操作成功'
    })
