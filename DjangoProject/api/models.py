from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """扩展用户资料"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 用 CharField 兼容 H5/小程序本地路径、网络 URL
    avatar = models.CharField(max_length=500, blank=True, default='')
    signature = models.CharField(max_length=120, blank=True, default='')

    def __str__(self):
        return f'Profile({self.user.username})'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
