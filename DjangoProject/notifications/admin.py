from django.contrib import admin
from .models import Notification  # 导入通知模型

# 注册模型到Admin后台
admin.site.register(Notification)