from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, login_view, logout_view, toggle_like, post_comments, update_avatar, update_nickname, update_signature, update_password
from .utils import health_check, api_info
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('info/', api_info, name='api-info'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('', include(router.urls)),
  
    # 注册搜索模块
    path('', include('api.search.urls')),
  
    # 帖子相关接口（与发现页共享）
    # create_post已移除，由publish应用处理
    path('posts/<int:post_id>/like/', toggle_like, name='toggle-like'),
    path('posts/<int:post_id>/comments/', post_comments, name='post-comments'),
    
    # 用户相关接口
    path('user/avatar/', update_avatar, name='update-avatar'),
    path('user/nickname/', update_nickname, name='update-nickname'),
    path('user/signature/', update_signature, name='update-signature'),
    path('user/password/', update_password, name='update-password'),
]
