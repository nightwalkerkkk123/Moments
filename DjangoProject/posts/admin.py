from django.contrib import admin
from .models import Post, Comment, Like  # 导入我们创建的3个模型

# 注册模型到Admin后台
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)