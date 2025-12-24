"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # 获取Token（登录）
    TokenRefreshView,     # 刷新Token
)

urlpatterns = [
    path('admin/', admin.site.urls),  # Django后台管理地址
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 登录接口
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新Token接口
    path('api/', include('publish.urls')),  # 发布应用接口移到api应用之前，确保create_post优先匹配
    path('api/', include('api.urls')),
    path('api/setting/', include('setting.urls')),
    path('api/user/', include('my.urls')),  # 我的应用接口
    path('api/posts/', include('posts.urls')),  # 发现应用接口
    path('api/notifications/', include('notifications.urls')),  # 通知应用接口
]

# Add media files URL configuration for development environment
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
