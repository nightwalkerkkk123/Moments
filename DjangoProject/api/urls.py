from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, login_view, logout_view
from .utils import health_check, api_info

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('info/', api_info, name='api-info'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('', include(router.urls)),
]