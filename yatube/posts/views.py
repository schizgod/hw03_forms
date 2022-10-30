from core.paginator import get_page_context
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    posts = Post.objects.select_related("group", "author")
    page_obj = get_page_context(request, posts)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author')
    page_obj = get_page_context(request, posts)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('author', 'group')
    posts_count = posts.count()
    page_obj = get_page_context(request, posts)
    context = {
        'author': author,
        'posts_count': posts_count,
        'page_obj': page_obj
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    posts_count = post.author.posts.count()
    context = {
        'post': post,
        'posts_count': posts_count
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', request.user)

    context = {'form': form}
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user.id != post.author.id:
        return redirect("posts:post_detail", post.pk)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        post.text = form.cleaned_data['text']
        post.group = form.cleaned_data['group']
        post.save()
        form.save()
        return redirect('posts:post_detail', post_id)

    context = {'form': form, 'is_edit': True, 'post': post}
    return render(request, 'posts/create_post.html', context)
