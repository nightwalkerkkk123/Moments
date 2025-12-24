from rest_framework import viewsets, status, pagination
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer, UserCreateSerializer, PostSerializer, CommentSerializer, CreateCommentSerializer
from .models import Post, Like, Comment


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # 默认允许匿名访问
    
    def get_permissions(self):
        """根据动作设置不同的权限"""
        if self.action in ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy', 'me']:
            return [IsAuthenticated()]  # 列表、详情、创建、更新、删除和获取当前用户信息需要认证
        return [AllowAny()]  # register 允许匿名访问
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def create(self, request, *args, **kwargs):
        """重写创建方法，使用注册逻辑"""
        return self.register(request)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """获取当前用户信息"""
        # 添加调试信息
        print(f"请求头: {request.META}")
        print(f"用户认证: {request.user}")
        print(f"用户是否认证: {request.user.is_authenticated}")
        
        serializer = self.get_serializer(request.user)
        return Response({
            'success': True,
            'message': '获取用户信息成功',
            'data': serializer.data
        })
    
    @action(detail=False, methods=['post', 'get'], permission_classes=[AllowAny])
    def register(self, request):
        """用户注册"""
        if request.method == 'GET':
            return Response({
                'message': 'This is the user registration endpoint.',
                'method': 'POST',
                'required_fields': ['username', 'password'],
                'optional_fields': ['email', 'first_name', 'last_name'],
                'example': {
                    'username': 'newuser',
                    'password': 'securepassword',
                    'email': 'user@example.com'
                }
            })
        
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User created successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt  # Added to disable CSRF for login
def login_view(request):
    """用户登录接口"""
    # 添加调试信息
    print(f"请求方法: {request.method}")
    print(f"请求头: {request.headers}")
    print(f"请求数据: {request.data}")
    print(f"用户认证: {request.user}")
    print(f"CSRF令牌: {request.COOKIES.get('csrftoken')}")
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Please provide both username and password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'Login successful',
            'token': token.key,
            'user': UserSerializer(user).data
        })
    else:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout_view(request):
    """用户登出接口"""
    try:
        # 获取token
        token_key = request.META.get('HTTP_AUTHORIZATION')
        if token_key:
            # 提取token值（去掉'Token '前缀）
            token_value = token_key.split(' ')[1] if len(token_key.split(' ')) > 1 else token_key
            # 删除用户的 token
            Token.objects.filter(key=token_value).delete()
        
        return Response({
            'success': True,
            'message': 'Logout successful'
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Logout failed: {}'.format(str(e))
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 自定义分页类
class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'pageSize'
    max_page_size = 100

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_avatar(request):
    """更新用户头像接口"""
    try:
        avatar = request.data.get('avatar')
        if not avatar:
            return Response({
                'success': False,
                'message': '头像不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新用户头像
        user = request.user
        user.profile.avatar = avatar
        user.profile.save()
        
        return Response({
            'success': True,
            'message': '头像更新成功',
            'data': {
                'avatar': user.profile.avatar
            }
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'头像更新失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_nickname(request):
    """更新用户昵称接口"""
    try:
        nickname = request.data.get('nickname')
        if not nickname:
            return Response({
                'success': False,
                'message': '昵称不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if len(nickname) < 2 or len(nickname) > 20:
            return Response({
                'success': False,
                'message': '昵称长度必须在2-20个字符之间'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新用户昵称
        user = request.user
        user.username = nickname
        user.save()
        
        return Response({
            'success': True,
            'message': '昵称更新成功',
            'data': {
                'nickname': user.username
            }
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'昵称更新失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_signature(request):
    """更新用户个性签名接口"""
    try:
        signature = request.data.get('signature', '')
        
        if len(signature) > 60:
            return Response({
                'success': False,
                'message': '个性签名不能超过60个字符'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新用户个性签名
        user = request.user
        user.profile.signature = signature
        user.profile.save()
        
        return Response({
            'success': True,
            'message': '个性签名更新成功',
            'data': {
                'signature': user.profile.signature
            }
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'个性签名更新失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_password(request):
    """更新用户密码接口"""
    try:
        old_password = request.data.get('oldPassword')
        new_password = request.data.get('newPassword')
        confirm_password = request.data.get('confirmPassword')
        
        if not old_password or not new_password or not confirm_password:
            return Response({
                'success': False,
                'message': '请填写完整信息'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if new_password != confirm_password:
            return Response({
                'success': False,
                'message': '两次输入的密码不一致'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if len(new_password) < 6:
            return Response({
                'success': False,
                'message': '新密码至少需要6个字符'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新用户密码
        user = request.user
        if not user.check_password(old_password):
            return Response({
                'success': False,
                'message': '原密码错误'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        
        return Response({
            'success': True,
            'message': '密码更新成功'
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'密码更新失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, post_id):
    """点赞/取消点赞接口"""
    try:
        post = Post.objects.get(id=post_id)
        liked = request.data.get('liked', True)
        
        if liked:
            # 点赞
            like, created = Like.objects.get_or_create(user=request.user, post=post)
            if not created:
                # 已经点赞过
                return Response({
                    'success': False,
                    'message': '已经点赞过'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 取消点赞
            try:
                like = Like.objects.get(user=request.user, post=post)
                like.delete()
            except Like.DoesNotExist:
                return Response({
                    'success': False,
                    'message': '未点赞过该动态'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新点赞数
        post.refresh_from_db()
        
        return Response({
            'success': True,
            'message': '操作成功',
            'data': {
                'likes': post.likes_count
            }
        })
    except Post.DoesNotExist:
        return Response({
            'success': False,
            'message': '动态不存在'
        }, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_comments(request, post_id):
    """获取动态评论列表和发布评论接口"""
    try:
        post = Post.objects.get(id=post_id)
        
        if request.method == 'GET':
            # 获取评论列表
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('pageSize', 10)
            
            # 按时间倒序获取评论
            comments = Comment.objects.filter(post=post).order_by('-created_at')
            
            # 分页
            paginator = StandardResultsSetPagination()
            paginator.page_size = page_size
            result_page = paginator.paginate_queryset(comments, request)
            
            # 序列化
            serializer = CommentSerializer(result_page, many=True, context={'request': request})
            
            return paginator.get_paginated_response({
                'success': True,
                'data': {
                    'comments': serializer.data,
                    'total': comments.count()
                }
            })
        elif request.method == 'POST':
            # 发布评论
            serializer = CreateCommentSerializer(data=request.data)
            
            if serializer.is_valid():
                comment = serializer.save(user=request.user, post=post)
                
                # 序列化返回的评论
                comment_serializer = CommentSerializer(comment, context={'request': request})
                
                return Response({
                    'success': True,
                    'message': '评论成功',
                    'data': comment_serializer.data
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'success': False,
                'message': '评论失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    except Post.DoesNotExist:
        return Response({
            'success': False,
            'message': '动态不存在'
        }, status=status.HTTP_404_NOT_FOUND)
