from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# Create your models here.
# 创建一个manager
class ArticleManager(models.Manager):
    def get_queryset(self):
        return super(ArticleManager, self).get_queryset().filter(status="published")


# 创建文章
class Article(models.Model):
    # 状态选择：草稿或是已发布
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    # 标称
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
    manager = ArticleManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail',
                       args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    def get_comment_list(self, comments):
        # 1.首先循环评论列表，找出父级评论，将父级评论加入到一个空列表中
        # 2.循环判断父级列表中的每一个父级对象是否有comment_children[]属性，如果没有，则为其添加，
        # 如果有就判断父级对象的parent_id和评论的id是否一样，一样就把评论添加到父级对象的子列表中
        comment_list = []
        # 循环查询结果
        for comment in comments:
            # 根据parent_id是否为none来判断是否是父评论，如果是父评论，就将评论追加到列表中
            if comment.parent_id is None:
                comment_list.append(comment)
            # 如果不是父评论，就循环已经盛有父评论的列表
            for child_comment in comment_list:
                # 判断父评论是否具有comment_children属性，如果没有属性，则添加该属性
                if not hasattr(child_comment, 'comment_children'):
                    setattr(child_comment, 'comment_children', [])
                # 判断当前父评论的id和当前子评论的parent_id是否一致，如果一致，说明两条评论时父子关系，再将子评论追加到子列表中
                if child_comment.id == comment.parent_id:
                    child_comment.comment_children.append(comment)
        return comment_list


# 评论包含：id,article_id,userid,parent_id,create_time,content
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_id = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=100)
    comment_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{},{},{},{},{}".format(self.article.id, self.user.id, self.parent_id, self.content, self.comment_time)

    # class Meta:
    #     ordering = ['-id']
