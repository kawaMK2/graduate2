from django.db import models
from accounts.models import User


class Tag(models.Model):
    """
    Note:
        Noteに関連付けするTagのモデル

    Attributes:
        name
    """
    name = models.CharField(max_length=255, unique=True)


class Note(models.Model):
    """
    Note:
        Noteのモデル本体
        このモデルに関連づけられたUserモデルは削除できない
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    locate = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    elapsed_time = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    tag = models.ManyToManyField(Tag)
    text_type = models.IntegerField()
    has_metadata = models.BooleanField(default=False)

    def tag_list(self):
        # Noteに含まれるtagを一つのstrとして取得する謎関数
        tags = []
        for tag in self.tag.all():
            tags.append(tag.name)
        return ', '.join(tags)


class Comment(models.Model):
    """
    Note:
        Noteに対して投稿できるコメントのモデル
        userとanonymousはgraduate2から新規。旧graduateからのデータ引き継ぎのためにuserのnull=True
    """
    name = models.CharField(max_length=100)
    content = models.TextField()
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    anonymous = models.BooleanField(default=False)
    posted_date = models.DateTimeField()
