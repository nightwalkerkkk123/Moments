# Django 纯后端 API 服务

这是一个配置为纯后端 API 服务的 Django 项目，专为前后端分离架构设计。



## API 端点

### 公开接口（无需认证）

- `GET /api/health/` - 健康检查
- `GET /api/info/` - API 信息
- `GET /api/users/register/` - 注册接口信息
- `POST /api/users/register/` - 用户注册
- `POST /api/auth/login/` - 用户登录

### 需要认证的接口

#### 用户相关
- `GET /api/users/` - 用户列表
- `GET /api/users/{id}/` - 获取用户详情
- `POST /api/users/` - 创建用户（等同于注册）
- `PUT /api/users/{id}/` - 更新用户信息
- `DELETE /api/users/{id}/` - 删除用户
- `GET /api/user/current/` - 获取当前用户信息
- `POST /api/auth/logout/` - 用户登出

#### 动态相关
- `POST /api/posts/` - 发布动态
- `GET /api/user/posts/` - 获取我的动态
- `DELETE /api/user/posts/{post_id}/` - 删除我的动态

#### 文件上传
- `POST /api/upload/image/` - 上传图片
- `POST /api/upload/video/` - 上传视频

#### 标签相关
- `GET /api/tags/common/` - 获取常用标签
- `POST /api/tags/` - 创建标签

#### 互动相关
- `POST /api/posts/{post_id}/like/` - 点赞/取消点赞
- `GET /api/posts/{post_id}/comments/` - 获取评论
- `POST /api/posts/{post_id}/comments/` - 创建评论

#### 统计相关
- `GET /api/user/stats/` - 获取我的统计信息

#### 通知相关
- `GET /api/notifications/` - 获取通知列表
- `PUT /api/notifications/{notification_id}/read/` - 标记单个通知为已读
- `PUT /api/notifications/read-all/` - 标记所有通知为已读
- `DELETE /api/notifications/{notification_id}/delete/` - 删除单个通知
- `DELETE /api/notifications/delete-all/` - 删除所有通知

## 配置说明



### 1. 添加了 REST Framework
- 配置了 JSON 渲染器和解析器
- 设置了认证和权限类
- 启用了分页和过滤功能

### 2. 数据库
- 使用 SQLite 作为开发数据库
- 已配置好用户认证相关表

## 环境准备

### 1. 安装依赖

首先安装项目所需的 Python 依赖包：

```bash
pip install -r requirements.txt
```

### 2. 数据库迁移

运行数据库迁移命令创建必要的表结构：

```bash
python manage.py migrate
```

## 启动服务

```bash
python manage.py runserver 8000
```

服务将在 http://127.0.0.1:8000 启动

## 测试账号

已创建的测试账号：
- **用户名**: testuser
- **密码**: testpass123

此账号可用于测试登录和认证功能。



### 认证方式
1. **Token 认证**: 在请求头中添加 `Authorization: Token your-token`
2. **Session 认证**: 先登录获取 session，后续请求会自动携带 cookie

### 权限说明
- **公开接口**: 无需任何认证即可访问，适合健康检查、用户注册等
- **认证接口**: 需要提供有效的认证凭据才能访问，适合用户管理、数据操作等
