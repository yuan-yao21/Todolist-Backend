from django.db import models
from user.models import User

def user_directory_path(instance, filename):
    base_path = 'upload/{username}'.format(username=instance.user.username)
    return '{}/{}'.format(base_path, filename)

# Create your models here.
class Note(models.Model):
    """
    单条笔记
    """

    category = models.CharField(max_length=32, verbose_name="笔记类别")
    
    title = models.CharField(max_length=255, verbose_name="标题")
    textContent = models.TextField(verbose_name="文本内容")

    picture = models.ImageField(upload_to=user_directory_path, verbose_name="图片", blank=True, null=True)
    audio = models.FileField(upload_to=user_directory_path, verbose_name="音频", blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, verbose_name="笔记创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="笔记更新时间")

    user = models.ForeignKey("user.User", on_delete=models.CASCADE, verbose_name="用户")
