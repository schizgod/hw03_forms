from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.utils import paginate
from posts.forms import PostForm
from posts.models import Group, Post, User
from yatube.settings import POSTS_NUMBER


def index(request):
    page_obj = paginate(
        request, POSTS_NUMBER, Post.objects.select_related('group').all(),
    )
    return render(
        request,
        'posts/index.html',
        {
            'page_obj': page_obj,
        },
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    page_obj = paginate(
        request, POSTS_NUMBER, group.posts.select_related('author').all(),
    )
    return render(
        request,
        'posts/group_list.html',
        {
            'group': group,
            'page_obj': page_obj,
        },
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    page_obj = paginate(
        request, POSTS_NUMBER, author.posts.all(),
    )  # переименовано. изменить в шаблоне
    return render(
        request,
        'posts/profile.html',
        {
            'author': author,
            'page_obj': page_obj,
        },
    )


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(
        request,
        'posts/post_detail.html',
        {
            'post': post,
        },
    )


@login_required
def post_create(request):
    group = Group.objects.all()
    form = PostForm(request.POST or None)
    if request.method != 'POST' or not form.is_valid():
        form = PostForm(None)
        return render(
            request,
            'posts/create_post.html',
            {
                'form': form,
                'group': group,
            },
        )
    if request.method == 'POST':
        form = PostForm(request.POST)
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('posts:profile', request.user)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None, instance=post)
    if request.method != 'POST':
        return render(
            request,
            'posts/create_post.html',
            {'form': form, 'is_edit': True, 'post': post},
        )
    if request.user.id != post.author.id:
        return redirect('posts:post_detail', post.pk)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        return redirect('posts:post_detail', post_id=post_id)
