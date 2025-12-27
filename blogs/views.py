from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import BlogPost, Comment, Tag
from .forms import BlogPostForm, CommentForm


def index(request):
    """主页：显示所有文章（分页）"""
    posts_list = BlogPost.objects.all()
    paginator = Paginator(posts_list, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blogs/index.html', {'posts': posts})


def post_detail(request, post_id):
    """文章详情页"""
    post = get_object_or_404(BlogPost, id=post_id)

    # 增加浏览量
    post.views += 1
    post.save(update_fields=['views'])

    # 评论表单
    comment_form = CommentForm()

    # 检查用户是否已点赞
    is_liked = False
    if request.user.is_authenticated:
        is_liked = post.likes.filter(id=request.user.id).exists()

    context = {
        'post': post,
        'comment_form': comment_form,
        'is_liked': is_liked,
    }
    return render(request, 'blogs/post_detail.html', context)


@login_required
def new_post(request):
    """新建文章"""
    if request.method != 'POST':
        form = BlogPostForm()
    else:
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            form.save()  # 保存标签
            messages.success(request, '文章发布成功！')
            return redirect('blogs:index')

    return render(request, 'blogs/new_post.html', {'form': form})


@login_required
def edit_post(request, post_id):
    """编辑文章"""
    post = get_object_or_404(BlogPost, id=post_id)

    if post.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = BlogPostForm(instance=post)
        # 填充现有标签
        form.initial['tags_input'] = ', '.join([t.name for t in post.tags.all()])
    else:
        form = BlogPostForm(instance=post, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '文章更新成功！')
            return redirect('blogs:post_detail', post_id=post.id)

    return render(request, 'blogs/edit_post.html', {'post': post, 'form': form})


@login_required
def delete_post(request, post_id):
    """删除文章"""
    post = get_object_or_404(BlogPost, id=post_id)

    if post.owner != request.user:
        raise Http404

    if request.method == 'POST':
        post.delete()
        messages.success(request, '文章已删除！')
        return redirect('blogs:index')

    return render(request, 'blogs/delete_post.html', {'post': post})


# ========== 评论功能 ==========

@login_required
def add_comment(request, post_id):
    """添加评论"""
    post = get_object_or_404(BlogPost, id=post_id)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, '评论发表成功！')

    return redirect('blogs:post_detail', post_id=post_id)


@login_required
def delete_comment(request, comment_id):
    """删除评论"""
    comment = get_object_or_404(Comment, id=comment_id)

    # 只能删除自己的评论
    if comment.author != request.user:
        raise Http404

    post_id = comment.post.id
    comment.delete()
    messages.success(request, '评论已删除！')
    return redirect('blogs:post_detail', post_id=post_id)


# ========== 点赞功能 ==========

@login_required
def like_post(request, post_id):
    """点赞/取消点赞"""
    post = get_object_or_404(BlogPost, id=post_id)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    # 支持 AJAX 请求
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})

    return redirect('blogs:post_detail', post_id=post_id)


# ========== 搜索功能 ==========

def search(request):
    """搜索文章"""
    query = request.GET.get('q', '')
    posts = []

    if query:
        posts = BlogPost.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
        )

    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'blogs/search_results.html', context)


# ========== 标签功能 ==========

def tag_posts(request, tag_name):
    """按标签筛选文章"""
    tag = get_object_or_404(Tag, name=tag_name)
    posts = tag.posts.all()

    context = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, 'blogs/tag_posts.html', context)


# ========== 用户主页 ==========

def user_profile(request, username):
    """用户个人主页"""
    user = get_object_or_404(User, username=username)

    # 用户的文章
    user_posts = BlogPost.objects.filter(owner=user)
    # 用户收藏的文章
    liked_posts = user.liked_posts.all()
    # 统计信息
    stats = {
        'post_count': user_posts.count(),
        'liked_count': liked_posts.count(),
        'comment_count': Comment.objects.filter(author=user).count(),
    }

    context = {
        'profile_user': user,
        'user_posts': user_posts,
        'liked_posts': liked_posts,
        'stats': stats,
    }
    return render(request, 'blogs/user_profile.html', context)
