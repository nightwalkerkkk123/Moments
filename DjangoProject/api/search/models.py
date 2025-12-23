from django.db import models
####################  搜索部分开始  ######################
from django.contrib.auth import get_user_model
User = get_user_model()

# --------------- 1.Post  ---------------
class Post(models.Model):
    """动态/朋友圈"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField()
    type = models.CharField(max_length=10, choices=[('image','image'),('video','video')])
    media = models.JSONField(default=list, blank=True)   # ["url1","url2"]
    tag  = models.CharField(max_length=20, blank=True)
    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

# --------------- 2.搜索历史  ---------------
class SearchHistory(models.Model):
    """用户搜索历史"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=50)
    tag = models.CharField(max_length=20, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
####################  搜索部分结束  ######################