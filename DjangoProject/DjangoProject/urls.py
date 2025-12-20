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
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # 获取Token（登录）
    TokenRefreshView,     # 刷新Token
)

urlpatterns = [
    #    path("admin/", admin.site.urls),
    path('admin/', admin.site.urls),  # Django后台管理地址
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 登录接口
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新Token接口
    path('api/', include('api.urls')),
    path('api/posts/', include('posts.urls')),  # 包含posts应用的接口
    path('api/notifications/', include('notifications.urls')),  # 包含notifications应用的接口
]
