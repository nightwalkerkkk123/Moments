from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserCreateSerializer

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
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
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
def login_view(request):
    """用户登录接口"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Please provide both username and password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # 获取或创建 token
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
@permission_classes([IsAuthenticated])
def logout_view(request):
    """用户登出接口"""
    try:
        # 删除用户的 token
        Token.objects.filter(user=request.user).delete()
        return Response({
            'message': 'Logout successful'
        })
    except Token.DoesNotExist:
        return Response({
            'message': 'No active session found'
        }, status=status.HTTP_400_BAD_REQUEST)
