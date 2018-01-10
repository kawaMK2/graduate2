# coding=utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import models as auth_models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Grade(models.Model):
    """
    Note:
        学年モデル
        Userが複数個のモデルを持つ
        priorityが高いものが現在のUserの学年
    """
    name = models.CharField(max_length=100)
    formal_name = models.CharField(max_length=100)
    priority = models.IntegerField()


class User(AbstractUser):
    """
    Note:
        Userオブジェクトについて参考：
        https://docs.djangoproject.com/ja/2.0/topics/auth/customizing/

        avatarとthumbnailはgraduate2から新規
    """
    belongs = models.ManyToManyField(Grade, through='Belong')
    objects = auth_models.UserManager()
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True)
    thumbnail = ImageSpecField(source='avatar', processors=[ResizeToFill(800, 800)], format='PNG', options={'quality': 90})

    def get_full_name(self):
        return '%s %s' % (self.last_name, self.first_name)


class Belong(models.Model):
    """
    Note:
        throughモデル
        belongsの役割について参考:
        https://docs.djangoproject.com/ja/2.0/topics/db/models/
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    start_time = models.DateField()
    end_time = models.DateField(null=True, blank=True)
