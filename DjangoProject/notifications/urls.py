from django.urls import path
from .views import NotificationListView, MarkAsReadView

urlpatterns = [
    # 1. 去掉路由前缀"notifications"（主urls已挂载/api/notifications/，重复会导致路径错误）
    # 2. 末尾加斜杠（和其他接口保持一致，避免APPEND_SLASH冲突）
    path('', NotificationListView.as_view(), name='notification-list'),  # 获取通知：对应 /api/notifications/
    path('mark-as-read/', MarkAsReadView.as_view(), name='mark-as-read'),  # 标记已读：对应 /api/notifications/mark-as-read/
]