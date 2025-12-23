from django.urls import path
from .views import (
    get_notifications,
    mark_notification_read,
    mark_all_notifications_read,
    delete_notification,
    delete_all_notifications
)

app_name = 'notifications'

urlpatterns = [
    # 获取通知列表
    path('', get_notifications, name='get_notifications'),  # 对应 /api/notifications/
    # 标记单个通知为已读
    path('<int:notification_id>/read/', mark_notification_read, name='mark_notification_read'),  # 对应 /api/notifications/<id>/read/
    # 标记所有通知为已读
    path('read-all/', mark_all_notifications_read, name='mark_all_notifications_read'),  # 对应 /api/notifications/read-all/
    # 删除单个通知
    path('<int:notification_id>/delete/', delete_notification, name='delete_notification'),  # 对应 /api/notifications/<id>/delete/
    # 删除所有通知
    path('delete-all/', delete_all_notifications, name='delete_all_notifications'),  # 对应 /api/notifications/delete-all/
]
