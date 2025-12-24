import os
import uuid
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from api.models import Post, Tag
from api.serializers import PostSerializer
from .serializers import CreatePostSerializer, CreateTagSerializer, CurrentUserSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    """发布动态接口"""
    serializer = CreatePostSerializer(data=request.data)
    
    if serializer.is_valid():
        validated_data = serializer.validated_data
        user = request.user
        
        # 确定动态类型
        post_type = 'text'
        media = []
        
        # 处理图片
        images = validated_data.get('images', [])
        if images:
            post_type = 'image'
            media.extend(images)
        
        # 处理视频
        video = validated_data.get('video', '')
        video_poster = validated_data.get('videoPoster', '')
        if video:
            post_type = 'video'
            media.append(video)
            if video_poster:
                media.append(video_poster)
        
        # 创建动态
        post = Post.objects.create(
            user=user,
            text=validated_data.get('text', ''),
            type=post_type,
            media=media
        )
        
        # 处理标签
        tags = validated_data.get('tags', [])
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name.strip())
            post.tags.add(tag)
        
        # 序列化返回结果
        post_serializer = PostSerializer(post, context={'request': request})
        return Response({
            'success': True,
            'message': '发布成功',
            'data': post_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': '发布失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request):
    """图片上传接口"""
    if 'file' not in request.FILES:
        return Response({
            'success': False,
            'message': '请提供图片文件'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['file']
    
    # 生成唯一文件名
    file_extension = os.path.splitext(file.name)[1]
    filename = f"{uuid.uuid4()}{file_extension}"
    
    # 保存文件
    file_path = os.path.join('uploads', 'images', filename)
    file_content = ContentFile(file.read())
    
    # 在开发环境中，我们使用本地存储
    # 在生产环境中，应该使用云存储服务
    file_url = f"/media/{file_path}"
    
    # 保存文件
    default_storage.save(file_path, file_content)
    
    return Response({
        'success': True,
        'data': {
            'url': file_url
        }
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_video(request):
    """视频上传接口"""
    if 'file' not in request.FILES:
        return Response({
            'success': False,
            'message': '请提供视频文件'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['file']
    
    # 生成唯一文件名
    file_extension = os.path.splitext(file.name)[1]
    filename = f"{uuid.uuid4()}{file_extension}"
    
    # 保存文件
    file_path = os.path.join('uploads', 'videos', filename)
    file_content = ContentFile(file.read())
    
    # 在开发环境中，我们使用本地存储
    # 在生产环境中，应该使用云存储服务
    file_url = f"/media/{file_path}"
    
    # 保存文件
    default_storage.save(file_path, file_content)
    
    # 视频封面URL（在实际应用中，应该生成视频封面）
    video_poster_url = f"/media/uploads/videos/{uuid.uuid4()}.jpg"
    
    return Response({
        'success': True,
        'data': {
            'url': file_url,
            'poster': video_poster_url
        }
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_common_tags(request):
    """获取常用标签接口"""
    # 定义一些常用标签
    common_tags = ['户外', '日常', '美食', '旅行', '运动', '摄影', '读书', '音乐', '电影', '宠物', '工作', '学习']
    
    # 确保这些标签存在于数据库中
    for tag_name in common_tags:
        Tag.objects.get_or_create(name=tag_name)
    
    return Response({
        'success': True,
        'data': {
            'tags': common_tags
        }
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tag(request):
    """创建新标签接口"""
    serializer = CreateTagSerializer(data=request.data)
    
    if serializer.is_valid():
        tag, created = Tag.objects.get_or_create(name=serializer.validated_data['name'])
        
        if not created:
            return Response({
                'success': False,
                'message': '标签已存在'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'success': True,
            'message': '标签创建成功',
            'data': {
                'id': tag.id,
                'name': tag.name
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': '标签创建失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """获取当前用户信息接口"""
    serializer = CurrentUserSerializer(request.user)
    return Response({
        'success': True,
        'data': serializer.data
    })
