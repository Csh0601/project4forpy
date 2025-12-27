from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    # 基础功能
    path('', views.index, name='index'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('new_post/', views.new_post, name='new_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),

    # 评论功能
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    # 点赞功能
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),

    # 搜索功能
    path('search/', views.search, name='search'),

    # 标签功能
    path('tag/<str:tag_name>/', views.tag_posts, name='tag_posts'),

    # 用户主页
    path('user/<str:username>/', views.user_profile, name='user_profile'),
]
