from django.db import models

# Create your models here.
class User(models.Model):
    """
    记事本用户
    """

    username = models.CharField(max_length=32, unique=True, blank=False, verbose_name="用户名")
    password = models.CharField(max_length=50, blank=False, verbose_name="密码")
    
    nickname = models.CharField(max_length=50, blank=True, verbose_name="昵称")
    mobile = models.CharField(max_length=255, blank=True, verbose_name="手机号")
    bio = models.CharField(max_length=255, blank=True, verbose_name="个性签名")
    head_image = models.ImageField(upload_to='user_headImages/', blank=True, null=True, verbose_name="头像")

    created = models.DateTimeField(auto_now_add=True, verbose_name="用户信息创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="用户信息更新时间")
