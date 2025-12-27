from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    """标签模型"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """博客文章模型"""
    title = models.CharField(max_length=200)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # 高级功能字段
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    likes = models.ManyToManyField(User, blank=True, related_name='liked_posts')
    views = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # 文章封面图

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    """评论模型"""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author.username}: {self.content[:20]}'
