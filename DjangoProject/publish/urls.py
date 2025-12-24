from django.urls import path
from .views import (
    create_post,
    upload_image,
    upload_video,
    get_common_tags,
    create_tag,
    get_current_user,
)

urlpatterns = [
    # 发布动态相关接口
    path('posts/', create_post, name='create-post'),
    # 文件上传接口
    path('upload/image/', upload_image, name='upload-image'),
    path('upload/video/', upload_video, name='upload-video'),
    # 标签相关接口
    path('tags/common/', get_common_tags, name='get-common-tags'),
    path('tags/', create_tag, name='create-tag'),
    # 用户信息接口
    path('user/current/', get_current_user, name='get-current-user'),
]