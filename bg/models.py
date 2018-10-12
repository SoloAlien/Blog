from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
# 创建文章
class Article(models.Model):
    # 状态选择：草稿或是已发布
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    # 标签
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               related_name='blog_posts', on_delete=models.CASCADE)
    body = models.TextField()
    # auto_now无论是你添加还是修改对象，时间为你添加或者修改的时间
    # auto_now_add为添加时的时间，更新对象时不会有变动
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # 状态默认为草稿
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
