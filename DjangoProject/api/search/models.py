from django.db import models
####################  搜索部分开始  ######################
from django.contrib.auth import get_user_model
User = get_user_model()

# --------------- 搜索历史  ---------------
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