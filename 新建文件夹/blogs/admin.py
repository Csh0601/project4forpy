from django.contrib import admin
from .models import BlogPost, Tag, Comment


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'date_added', 'views']
    list_filter = ['date_added', 'owner', 'tags']
    search_fields = ['title', 'text']
    filter_horizontal = ['tags', 'likes']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['content']
