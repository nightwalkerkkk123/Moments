from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

class Notification(models.Model):
    TYPE_CHOICES = [
        ('like', '点赞'),
        ('comment', '评论')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)